import { useState } from 'react';
import { ArrowUp, ArrowDown, Info, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import type { Motion } from '@/types';
import { VoteBreakdown } from './VoteBreakdown';
import { cn } from '@/lib/utils';

interface MotionCardProps {
  motion: Motion;
  onVote: (motionId: string, vote: 'up' | 'down') => void;
  onInfoClick: (motionId: string) => void;
}

export function MotionCard({ motion, onVote, onInfoClick }: MotionCardProps) {
  const [localVote, setLocalVote] = useState<'up' | 'down' | undefined>(motion.userVote);

  const handleVote = (vote: 'up' | 'down') => {
    if (localVote === vote) {
      setLocalVote(undefined);
    } else {
      setLocalVote(vote);
      onVote(motion.id, vote);
    }
  };

  const statusColor = {
    'Passed': 'bg-vote-passed text-success-foreground',
    'Failed': 'bg-vote-failed text-destructive-foreground',
    'In Progress': 'bg-vote-progress text-warning-foreground'
  }[motion.status];

  return (
    <Card className="border-card-border hover:shadow-lg transition-shadow">
      <CardHeader className="space-y-3 pb-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 space-y-2">
            <h3 className="font-display text-lg font-semibold leading-tight text-foreground">
              {motion.title}
            </h3>
            <p className="text-sm text-muted-foreground line-clamp-2">
              {motion.description}
            </p>
          </div>
          <Badge className={cn('shrink-0', statusColor)}>
            {motion.status}
          </Badge>
        </div>

        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Calendar className="h-4 w-4" />
          <span>{new Date(motion.date).toLocaleDateString('en-CA', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}</span>
          <span className="mx-2">•</span>
          <span>
            Introduced by <span className="font-medium text-foreground">{motion.introducedBy.mpName}</span>
            {' '}({motion.introducedBy.party})
          </span>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {motion.categories.map(cat => (
            <Badge key={cat} variant="secondary" className="text-xs">
              {cat}
            </Badge>
          ))}
          <Badge variant="outline" className="text-xs">
            {motion.classification}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <VoteBreakdown votes={motion.voteBreakdown} />

        <div className="flex items-center justify-between pt-2 border-t border-border">
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleVote('up')}
              className={cn(
                'gap-1.5',
                localVote === 'up' && 'bg-success/10 border-success text-success hover:bg-success/20'
              )}
            >
              <ArrowUp className="h-4 w-4" />
              <span className="font-medium">{motion.upvotes}</span>
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleVote('down')}
              className={cn(
                'gap-1.5',
                localVote === 'down' && 'bg-destructive/10 border-destructive text-destructive hover:bg-destructive/20'
              )}
            >
              <ArrowDown className="h-4 w-4" />
              <span className="font-medium">{motion.downvotes}</span>
            </Button>
          </div>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => onInfoClick(motion.id)}
            className="gap-2 text-primary hover:text-primary-hover"
          >
            <Info className="h-4 w-4" />
            AI Explanation
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
