import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export const metadata = {
  title: "Contact — CogniESL",
  description: "Get in touch with the CogniESL team. Questions, feedback, or interested in a school plan?",
};

export default function ContactPage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">Contact</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Get in Touch
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Questions, feedback, or interested in a school plan? We&apos;d love to hear from you.
            </p>
          </div>
        </Container>
      </Section>

      <Section>
        <Container size="sm">
          <div className="bg-white dark:bg-neutral-900 rounded-2xl p-8 border border-neutral-200/80 dark:border-neutral-800 shadow-card">
            <form action="/api/contact" method="POST" className="space-y-5">
              <div className="grid sm:grid-cols-2 gap-4">
                <Input label="First Name" name="firstName" id="firstName" required placeholder="Sarah" />
                <Input label="Last Name" name="lastName" id="lastName" required placeholder="Johnson" />
              </div>
              <Input label="Email" name="email" id="email" type="email" required placeholder="sarah@school.edu" />
              <Input label="I am a..." name="role" id="role" placeholder="Teacher, Administrator, etc. (optional)" />
              <Input label="Subject" name="subject" id="subject" required placeholder="Question about CogniESL" />
              <Textarea label="Message" name="message" id="message" required rows={5} placeholder="Tell us how we can help..." />
              <Button type="submit" className="w-full" size="lg">Send Message</Button>
            </form>
          </div>

          <div className="grid sm:grid-cols-3 gap-4 mt-8">
            {[
              { icon: "📧", title: "Email", detail: "hello@cogniesl.com" },
              { icon: "🏫", title: "Schools", detail: "corporate@cogniesl.com" },
              { icon: "💬", title: "Response Time", detail: "Within 24 hours" },
            ].map((item) => (
              <div key={item.title} className="bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800 text-center">
                <div className="text-2xl mb-2">{item.icon}</div>
                <h3 className="text-sm font-semibold text-neutral-900 dark:text-neutral-100 mb-1">{item.title}</h3>
                <p className="text-sm text-neutral-500 dark:text-neutral-400">{item.detail}</p>
              </div>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
