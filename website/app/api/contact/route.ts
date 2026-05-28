import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const firstName = formData.get("firstName") as string;
    const lastName = formData.get("lastName") as string;
    const email = formData.get("email") as string;
    const subject = formData.get("subject") as string;
    const message = formData.get("message") as string;

    if (!firstName || !lastName || !email || !subject || !message) {
      return NextResponse.json(
        { error: "Please fill in all fields." },
        { status: 400 }
      );
    }

    if (!email.includes("@")) {
      return NextResponse.json(
        { error: "Please provide a valid email address." },
        { status: 400 }
      );
    }

    const { Resend } = await import("resend");
    const resend = new Resend(process.env.RESEND_API_KEY);

    await resend.emails.send({
      from: "CogniESL <noreply@cogniesl.com>",
      to: "marcos@cogniesl.com",
      replyTo: email,
      subject: `[Contact Form] ${subject}`,
      text: `Name: ${firstName} ${lastName}\nEmail: ${email}\n\n${message}`,
    });

    return NextResponse.json({
      success: true,
      message: "Thanks for reaching out! We'll get back to you within 24 hours.",
    });
  } catch (error) {
    console.error("[CONTACT] Error:", error);
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
