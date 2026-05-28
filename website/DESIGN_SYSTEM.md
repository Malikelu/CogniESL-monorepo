# CogniESL Design System

## Color Palette — "Warm Intelligence"

### Primary Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--primary` | `#0D7377` | Deep Teal — main brand color, headings, links, primary buttons |
| `--primary-light` | `#14919B` | Lighter teal — hover states, secondary elements |
| `--primary-dark` | `#095458` | Darker teal — active states, emphasis |

### Secondary Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--secondary` | `#FF6B6B` | Warm Coral — CTAs, accents, highlights, badges |
| `--secondary-light` | `#FF8E8E` | Lighter coral — hover states |
| `--secondary-dark` | `#E55A5A` | Darker coral — active states |

### Accent Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--accent` | `#F4A261` | Soft Gold — warmth, creativity, icons, decorative |
| `--accent-light` | `#F7B87A` | Lighter gold |
| `--accent-dark` | `#E08E4C` | Darker gold |

### Semantic Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--success` | `#2EC4B6` | Mint — success states, positive indicators |
| `--warning` | `#F4A261` | Gold — warnings |
| `--error` | `#FF6B6B` | Coral — errors |

### Neutral Colors (Light Mode)
| Token | Hex | Usage |
|-------|-----|-------|
| `--background` | `#FAFAF9` | Warm White — page background |
| `--surface` | `#FFFFFF` | White — cards, modals, surfaces |
| `--surface-hover` | `#F5F5F0` | Hover state for surfaces |
| `--border` | `#E5E5E0` | Light gray — borders, dividers |
| `--text-primary` | `#1A1A2E` | Dark Navy — headings, body text |
| `--text-secondary` | `#5A5A72` | Medium gray — subtext, captions |
| `--text-muted` | `#8A8A9A` | Muted gray — placeholders, disabled |

### Neutral Colors (Dark Mode)
| Token | Hex | Usage |
|-------|-----|-------|
| `--background` | `#0F0F1A` | Deep Navy — page background |
| `--surface` | `#1A1A2E` | Dark Navy — cards, modals |
| `--surface-hover` | `#252540` | Hover state for surfaces |
| `--border` | `#2A2A40` | Dark gray — borders, dividers |
| `--text-primary` | `#F0F0F5` | Off-white — headings, body text |
| `--text-secondary` | `#A0A0B8` | Medium gray — subtext, captions |
| `--text-muted` | `#6A6A80` | Muted gray — placeholders, disabled |

## Typography

### Font Families
```css
--font-heading: 'Inter', sans-serif;       /* Headings, navigation, buttons */
--font-body: 'Inter', sans-serif;          /* Body text, paragraphs */
--font-accent: 'Nunito', sans-serif;        /* Subtext, labels, friendly accents */
```

### Type Scale
| Level | Size (Desktop) | Size (Mobile) | Weight | Line Height | Usage |
|-------|----------------|---------------|--------|-------------|-------|
| `display` | 56px / 3.5rem | 36px / 2.25rem | 700 | 1.1 | Hero headlines |
| `h1` | 48px / 3rem | 32px / 2rem | 700 | 1.15 | Page titles |
| `h2` | 36px / 2.25rem | 28px / 1.75rem | 600 | 1.2 | Section titles |
| `h3` | 28px / 1.75rem | 22px / 1.375rem | 600 | 1.25 | Subsection titles |
| `h4` | 22px / 1.375rem | 18px / 1.125rem | 600 | 1.3 | Card titles |
| `h5` | 18px / 1.125rem | 16px / 1rem | 600 | 1.35 | Small headings |
| `body-lg` | 18px / 1.125rem | 16px / 1rem | 400 | 1.6 | Lead paragraphs |
| `body` | 16px / 1rem | 15px / 0.9375rem | 400 | 1.6 | Body text |
| `body-sm` | 14px / 0.875rem | 13px / 0.8125rem | 400 | 1.5 | Small text, captions |
| `caption` | 12px / 0.75rem | 12px / 0.75rem | 500 | 1.4 | Labels, badges, overlines |

## Spacing Scale
Based on 4px grid:
```
4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80, 96, 112, 128, 144, 160
```

## Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 6px | Small elements, tags |
| `--radius-md` | 10px | Buttons, inputs |
| `--radius-lg` | 16px | Cards, containers |
| `--radius-xl` | 24px | Large containers, modals |
| `--radius-full` | 9999px | Pills, avatars, badges |

## Shadows (Light Mode)
| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.06)` | Subtle elevation |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.08)` | Cards, dropdowns |
| `--shadow-lg` | `0 8px 30px rgba(0,0,0,0.10)` | Modals, floating elements |
| `--shadow-xl` | `0 20px 60px rgba(0,0,0,0.12)` | Hero elements |

## Shadows (Dark Mode)
| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.2)` | Subtle elevation |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.3)` | Cards, dropdowns |
| `--shadow-lg` | `0 8px 30px rgba(0,0,0,0.4)` | Modals, floating elements |
| `--shadow-xl` | `0 20px 60px rgba(0,0,0,0.5)` | Hero elements |

## Transitions
| Token | Value | Usage |
|-------|-------|-------|
| `--transition-fast` | `150ms ease` | Micro-interactions, hovers |
| `--transition-base` | `250ms ease` | Standard transitions |
| `--transition-slow` | `400ms ease` | Page transitions, complex animations |

## Breakpoints
| Token | Value |
|-------|-------|
| `sm` | 640px |
| `md` | 768px |
| `lg` | 1024px |
| `xl` | 1280px |
| `2xl` | 1536px |

## Component Patterns

### Buttons
- **Primary**: Teal background, white text, `--radius-md`, hover darkens
- **Secondary**: Coral background, white text, `--radius-md`, hover darkens
- **Outline**: Transparent with teal border, teal text, hover fills
- **Ghost**: Transparent, teal text, hover subtle background
- Sizes: sm (32px h), md (44px h), lg (52px h)

### Cards
- White/dark surface, `--radius-lg`, `--shadow-md`
- Hover: slight translateY(-2px) + shadow increase
- Padding: 24px (sm), 32px (md), 40px (lg)

### Navigation
- Sticky, blur backdrop, white/dark surface
- Height: 72px desktop, 64px mobile
- CTA button always visible

### Sections
- Max-width: 1200px centered
- Padding: 80px vertical (desktop), 56px (mobile)
- Alternating background colors for visual rhythm

## Animation Principles
- Scroll-triggered reveals (fade up, 300ms stagger)
- Hover micro-interactions (scale, color shift, shadow)
- L1 sandbox: typing animation with cursor blink
- Page transitions: fade through
- Reduced motion: respect `prefers-reduced-motion`
