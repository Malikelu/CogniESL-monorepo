import { NextRequest, NextResponse } from "next/server";

// CogniESL API base URL — set COGNIESL_API_URL in Railway/Vercel env vars.
// Falls back to the production URL so the website always works even if the var is missing.
const COGNIESL_API = process.env.COGNIESL_API_URL || "https://cogniesl-production.up.railway.app";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => null);
    const email = body?.email as string | undefined;

    if (!email || !email.includes("@")) {
      return NextResponse.json(
        { error: "Please provide a valid email address." },
        { status: 400 }
      );
    }

    // Forward the signup to the CogniESL API so it lands in the waitlist table.
    try {
      const res = await fetch(`${COGNIESL_API}/api/waitlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source: "website" }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        console.error("[WAITLIST] API error:", err);
        // Don't surface backend errors to the user — still show success.
      }
    } catch (fetchErr) {
      // Network failure reaching the API — log but don't fail the user.
      console.error("[WAITLIST] Could not reach CogniESL API:", fetchErr);
    }

    return NextResponse.json({
      success: true,
      message: "Thanks for joining the waitlist! We'll be in touch soon.",
    });
  } catch (error) {
    console.error("[WAITLIST] Error:", error);
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
