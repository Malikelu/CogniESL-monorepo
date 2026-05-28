import Link from "next/link";

const productLinks = [
  { href: "/how-it-works", label: "How It Works" },
  { href: "/samples", label: "Samples" },
  { href: "/pricing", label: "Pricing" },
  { href: "/about", label: "About" },
];

const companyLinks = [
  { href: "/contact", label: "Contact" },
];

const legalLinks = [
  { href: "/privacy", label: "Privacy Policy" },
  { href: "/terms", label: "Terms of Service" },
  { href: "/cookie-policy", label: "Cookie Policy" },
  { href: "/ai-disclaimer", label: "AI Disclaimer" },
];

export function Footer() {
  return (
    <footer className="bg-neutral-100 dark:bg-neutral-950 border-t border-neutral-200 dark:border-neutral-800" role="contentinfo">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="py-16">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
            <div className="lg:col-span-1">
              <Link href="/" className="flex items-center gap-2 text-xl font-bold mb-4">
                <img
                  src="/logo-wordmark-light.svg"
                  alt="CogniESL"
                  height={28}
                  className="h-[28px] w-auto hidden dark:hidden"
                />
                <img
                  src="/logo-wordmark-dark.svg"
                  alt="CogniESL"
                  height={28}
                  className="h-[28px] w-auto hidden dark:block"
                />
              </Link>
              <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4 max-w-xs">AI-powered lesson prep for ESL teachers. Built by a teacher, for teachers.</p>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-widest mb-4">Product</h4>
              <ul className="space-y-3">
                {productLinks.map((link) => (<li key={link.href}><Link href={link.href} className="text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors duration-150">{link.label}</Link></li>))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-widest mb-4">Company</h4>
              <ul className="space-y-3">
                {companyLinks.map((link) => (<li key={link.href}><Link href={link.href} className="text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors duration-150">{link.label}</Link></li>))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-widest mb-4">Legal</h4>
              <ul className="space-y-3">
                {legalLinks.map((link) => (<li key={link.href}><Link href={link.href} className="text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors duration-150">{link.label}</Link></li>))}
              </ul>
            </div>
          </div>
        </div>
        <div className="border-t border-neutral-200 dark:border-neutral-800 py-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-neutral-400">&copy; 2026 Cognicrafted. All rights reserved.</p>
          <p className="text-xs text-neutral-400 flex items-center gap-1.5">Powered by <a href="https://cognicrafted.com" target="_blank" rel="noopener noreferrer" className="text-primary-500 hover:text-primary-600 font-medium transition-colors">Cognicrafted</a></p>
        </div>
      </div>
    </footer>
  );
}
