import { Link } from 'react-router-dom';
import { Scale } from 'lucide-react';

export function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/80">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center gap-2 transition-opacity hover:opacity-80">
          <Scale className="h-7 w-7 text-accent-red" />
          <span className="font-display text-xl font-bold text-foreground">
            Rate<span className="text-accent-red">My</span>MP
          </span>
        </Link>
        
        <div className="flex items-center gap-6">
          <Link
            to="/"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            Recent Votes
          </Link>
          <Link
            to="/about"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            About
          </Link>
        </div>
      </div>
    </nav>
  );
}
