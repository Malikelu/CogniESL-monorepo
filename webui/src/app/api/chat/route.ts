import { NextRequest, NextResponse } from "next/server";

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

    const response = await fetch(`${openswarmUrl}/cogniesl/get_response`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`OpenSwarm error ${response.status}:`, errorText);
      return NextResponse.json(
        {
          error: "Backend error",
          response:
            "Sorry, I'm having trouble processing your request. Please try again.",
        },
        { status: 502 }
      );
    }

    const data = await response.json();
    return NextResponse.json({ response: data.response });
  } catch (error) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      {
        error: "Failed to process message",
        response:
          "Sorry, I'm having trouble connecting to the backend. Please try again later.",
      },
      { status: 500 }
    );
  }
}
