"use client";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import { AuthModal } from "@/components/AuthModal";

export function Navbar() {
  const { user, loading, saveToken, logout } = useAuth();
  const [showAuth, setShowAuth] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  // Prevent hydration mismatch: auth state comes from localStorage (client-only)
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  return (
    <>
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          {/* Logo — C-arc integrated wordmark */}
          <Link href="/" className="flex items-center">
            <svg height="32" viewBox="0 0 230 62" xmlns="http://www.w3.org/2000/svg" aria-label="CogniESL" role="img" style={{height: '32px', width: 'auto'}}>
              <path d="M 45,50 A 18,18 0 1,1 45,21" fill="none" stroke="#0b7272" strokeWidth="9" strokeLinecap="round"/>
              <line x1="45" y1="21" x2="57" y2="9" stroke="#1baa6e" strokeWidth="8" strokeLinecap="round"/>
              <text x="52" y="55" fontSize="38" fill="#0b7272" fontFamily="system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif" fontWeight="500">ogni</text>
              <text x="128" y="55" fontSize="38" fill="#1baa6e" fontFamily="system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif" fontWeight="500" letterSpacing="2">ESL</text>
            </svg>
          </Link>

          {/* Nav links */}
          <nav className="hidden sm:flex items-center gap-4">
            <Link href="/pricing" className="text-sm text-gray-500 hover:text-gray-900 transition-colors font-medium">
              Pricing
            </Link>
          </nav>

          {/* Right side */}
          <div className="flex items-center space-x-2">
            {mounted && !loading && !user && (
              <button
                onClick={() => setShowAuth(true)}
                className="text-sm font-medium text-teal hover:text-teal-dark transition-colors px-3 py-1.5 rounded-lg hover:bg-teal/5"
              >
                Sign in
              </button>
            )}

            {mounted && !loading && user && (
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900 transition-colors px-2 py-1.5 rounded-lg hover:bg-gray-100"
                >
                  <span className="w-7 h-7 rounded-full bg-teal/10 flex items-center justify-center text-teal font-semibold text-xs">
                    {user.email[0].toUpperCase()}
                  </span>
                  <span className="hidden sm:block max-w-[140px] truncate">{user.email}</span>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-gray-400">
                    <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
                  </svg>
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-1 w-44 bg-white border border-gray-200 rounded-xl shadow-lg py-1 z-40">
                    <Link
                      href="/materials"
                      className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-teal">
                        <path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" />
                      </svg>
                      My Materials
                    </Link>
                    <Link
                      href="/settings"
                      className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-gray-400">
                        <path fillRule="evenodd" d="M7.84 1.804A1 1 0 018.82 1h2.36a1 1 0 01.98.804l.331 1.652a6.993 6.993 0 011.929 1.115l1.598-.54a1 1 0 011.186.447l1.18 2.044a1 1 0 01-.205 1.251l-1.267 1.113a7.047 7.047 0 010 2.228l1.267 1.113a1 1 0 01.205 1.251l-1.18 2.044a1 1 0 01-1.186.447l-1.598-.54a6.993 6.993 0 01-1.929 1.115l-.33 1.652a1 1 0 01-.98.804H8.82a1 1 0 01-.98-.804l-.331-1.652a6.993 6.993 0 01-1.929-1.115l-1.598.54a1 1 0 01-1.186-.447l-1.18-2.044a1 1 0 01.205-1.251l1.267-1.113a7.047 7.047 0 010-2.228L1.821 7.773a1 1 0 01-.206-1.25l1.18-2.045a1 1 0 011.187-.447l1.598.54A6.992 6.992 0 017.51 3.456l.33-1.652zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                      </svg>
                      Settings
                    </Link>
                    <hr className="my-1 border-gray-100" />
                    <button
                      onClick={() => { logout(); setShowUserMenu(false); }}
                      className="flex items-center gap-2 w-full px-3 py-2 text-sm text-gray-500 hover:bg-gray-50 hover:text-gray-700"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                        <path fillRule="evenodd" d="M3 4.25A2.25 2.25 0 015.25 2h5.5A2.25 2.25 0 0113 4.25v2a.75.75 0 01-1.5 0v-2a.75.75 0 00-.75-.75h-5.5a.75.75 0 00-.75.75v11.5c0 .414.336.75.75.75h5.5a.75.75 0 00.75-.75v-2a.75.75 0 011.5 0v2A2.25 2.25 0 0110.75 18h-5.5A2.25 2.25 0 013 15.75V4.25z" clipRule="evenodd" />
                        <path fillRule="evenodd" d="M6 10a.75.75 0 01.75-.75h9.546l-1.048-.943a.75.75 0 111.004-1.114l2.5 2.25a.75.75 0 010 1.114l-2.5 2.25a.75.75 0 11-1.004-1.114l1.048-.943H6.75A.75.75 0 016 10z" clipRule="evenodd" />
                      </svg>
                      Sign out
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Online badge */}
            <span className="hidden sm:inline-flex items-center rounded-full bg-teal/10 px-3 py-1 text-xs font-medium text-teal">
              <span className="w-1.5 h-1.5 rounded-full bg-teal mr-1.5" />
              Online
            </span>
          </div>
        </div>
      </header>

      {showAuth && (
        <AuthModal
          onSuccess={(token, userData) => {
            saveToken(token, userData);
            setShowAuth(false);
          }}
          onClose={() => setShowAuth(false)}
        />
      )}
    </>
  );
}
