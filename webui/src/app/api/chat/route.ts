import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

function cleanResponse(text: string): string {
  text = text.replace(/<memory-context>[\s\S]*?<\/memory-context>/gi, "");
  text = text.replace(/\[System note:[\s\S]*?\]/gi, "");
  text = text.replace(/<memory-context>[\s\S]*/gi, "");
  text = text.replace(/\n{3,}/g, "\n\n").trim();
  return text;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, chat_history } = body;

    if (!message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    const openswarmUrl =
      process.env.OPENSWARM_URL || "http://localhost:8080";

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 120000);

    try {
      // Build the request body for OpenSwarm
      const openswarmBody: Record<string, unknown> = { message };
      if (chat_history && Array.isArray(chat_history)) {
        openswarmBody.chat_history = chat_history;
      }

      const response = await fetch(`${openswarmUrl}/cogniesl/get_response`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(openswarmBody),
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
      const cleaned = cleanResponse(data.response || "");
      return NextResponse.json({ response: cleaned });
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
