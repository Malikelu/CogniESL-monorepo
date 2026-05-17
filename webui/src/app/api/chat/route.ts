import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message } = body;

    if (!message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    const openswarmUrl =
      process.env.OPENSWARM_URL || "http://localhost:8080";

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 120000); // 2 min timeout

    try {
      const response = await fetch(`${openswarmUrl}/cogniesl/get_response`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`OpenSwarm error ${response.status}:`, errorText);
        return NextResponse.json(
          {
            response:
              "Sorry, I'm having trouble processing your request right now. Please try again in a moment.",
          },
          { status: 200 }
        );
      }

      const data = await response.json();
      return NextResponse.json({ response: data.response });
    } catch (fetchError) {
      clearTimeout(timeout);
      if (fetchError instanceof Error && fetchError.name === "AbortError") {
        return NextResponse.json(
          {
            response:
              "The request took too long. Please try again with a shorter message.",
          },
          { status: 200 }
        );
      }
      throw fetchError;
    }
  } catch (error) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      {
        response:
          "Sorry, I'm having trouble connecting to the backend. Please try again later.",
      },
      { status: 200 }
    );
  }
}
