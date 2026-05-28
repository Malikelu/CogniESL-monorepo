# CogniESL Product Systems Plan

## 1. Authentication System

### Provider: NextAuth.js v5 (Auth.js)
- Email/password for teachers
- Google OAuth (most teachers have Google accounts)
- Magic link option (passwordless)

### User Data Model
```
User {
  id: string
  email: string
  name: string
  role: 'teacher' | 'admin' | 'school_admin'
  school: string (optional)
  plan: 'free' | 'pro' | 'school'
  createdAt: datetime
  lastLogin: datetime
}

UserProfile {
  userId: string
  avatar: string (optional)
  bio: string (optional)
  languages: string[] (L1 languages they teach)
  teachingLevel: 'elementary' | 'middle' | 'high' | 'adult' | 'university'
  yearsExperience: number
  state: string (US state for compliance)
}
```

## 2. Payment System

### Provider: Stripe
- Stripe Checkout for initial subscription
- Stripe Customer Portal for management
- Stripe Billing for recurring payments

### Pricing Plans
```
Free:
  - 5 generations/month
  - 3 L1 languages
  - Worksheets & flashcards only
  - Basic difficulty levels

Pro ($12/month or $9/month annual):
  - Unlimited generations
  - All 31 L1 languages
  - All 6 material formats
  - All difficulty levels
  - Priority generation
  - Download as PPTX, PDF, DOCX
  - Save & organize materials

School (Custom pricing):
  - Everything in Pro
  - Admin dashboard
  - Teacher management (up to 50 teachers)
  - Usage analytics
  - SSO integration
  - Dedicated support
  - Invoice billing
```

### Stripe Integration
- Stripe Checkout for one-time and subscription payments
- Webhooks for subscription events (created, updated, cancelled)
- Stripe Customer Portal for self-service management
- Tax calculation with Stripe Tax

## 3. Data We Save (Useful for Us)

### Teaching Data
```
Generation {
  id: string
  userId: string
  type: 'worksheet' | 'slides' | 'flashcards' | 'conversation' | 'assessment' | 'lesson_plan'
  topic: string
  grammarPoint: string
  l1Language: string
  level: 'beginner' | 'intermediate' | 'advanced'
  content: JSON (the generated material)
  createdAt: datetime
  isFavorite: boolean
  tags: string[]
}

MaterialFolder {
  id: string
  userId: string
  name: string
  generations: string[]
  createdAt: datetime
}

SavedTemplate {
  id: string
  userId: string
  name: string
  config: JSON (generation parameters)
  createdAt: datetime
}
```

### Analytics Data (Privacy-Friendly)
```
UsageEvent {
  id: string
  userId: string (anonymous for free users)
  event: 'generation' | 'download' | 'signup' | 'login' | 'upgrade'
  metadata: JSON
  createdAt: datetime
}

AggregatedStats {
  totalGenerations: number
  generationsByType: JSON
  generationsByLanguage: JSON
  activeUsers: number
  conversionRate: number
  date: date
}
```

### Marketing Data
```
Waitlist {
  id: string
  email: string
  source: string (how they found us)
  referralCode: string (optional)
  createdAt: datetime
  notifiedAt: datetime (when we emailed them)
}

Referral {
  id: string
  referrerUserId: string
  referredEmail: string
  status: 'pending' | 'signed_up' | 'converted'
  createdAt: datetime
}
```

## 4. Database

### Provider: PostgreSQL via Supabase
- Free tier: 500MB database, 2GB bandwidth
- Built-in auth (can use alongside NextAuth)
- Real-time subscriptions
- Row Level Security for data protection

### Key Tables
- users
- user_profiles
- generations
- material_folders
- saved_templates
- subscriptions
- waitlist
- referrals
- usage_events

## 5. File Storage

### Provider: Supabase Storage
- Store generated materials (PPTX, PDF, DOCX)
- User avatars
- Free tier: 1GB storage

## 6. Email System

### Provider: Resend
- Transactional emails (welcome, password reset, etc.)
- Marketing emails (waitlist updates, launch announcement)
- Free tier: 3,000 emails/month

### Email Flows
1. Waitlist signup → confirmation email
2. Product launch → notify waitlist
3. User signup → welcome email
4. Weekly digest → teaching tips + new features
5. Subscription events → receipt, renewal, cancellation

## 7. Analytics

### Provider: Plausible (privacy-friendly, GDPR compliant)
- No cookies required
- No personal data collected
- Free tier: 10K pageviews/month
- Track: page views, conversions, referrers

### Custom Events Tracked
- Waitlist signup
- Generation created
- Material downloaded
- Plan upgraded
- Referral completed

## 8. Implementation Priority

### Phase 1: Auth + Payments
1. Set up NextAuth.js with Google OAuth
2. Set up Stripe with Checkout
3. Create user dashboard (basic)
4. Implement free/pro plan logic

### Phase 2: Core Product
1. Generation interface
2. Material storage and organization
3. Download functionality (PPTX, PDF, DOCX)
4. L1 intelligence integration

### Phase 3: School Features
1. Admin dashboard
2. Teacher management
3. Usage analytics
4. SSO integration

### Phase 4: Growth
1. Referral system
2. Email marketing
3. Content marketing (blog)
4. SEO optimization

## 9. Security Considerations

- All passwords hashed with bcrypt
- HTTPS everywhere
- CSRF protection via NextAuth
- Rate limiting on API routes
- Input validation with Zod
- SQL injection prevention via parameterized queries
- XSS prevention via React's built-in escaping
- Content Security Policy headers
- FERPA compliance (no student data collected)

## 10. Compliance

- FERPA: No student personal data collected
- COPPA: No data from children under 13
- GDPR: Privacy policy, data deletion right
- CCPA: California consumer privacy
- Stripe Tax: Automatic tax calculation
