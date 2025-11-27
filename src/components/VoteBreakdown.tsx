import type { PartyVote, PartyName } from '@/types';
import { cn } from '@/lib/utils';

interface VoteBreakdownProps {
  votes: PartyVote[];
}

const partyColors: Record<PartyName, string> = {
  'Liberal': 'bg-party-liberal',
  'Conservative': 'bg-party-conservative',
  'NDP': 'bg-party-ndp',
  'Bloc Québécois': 'bg-party-bloc',
  'Green': 'bg-party-green',
  'Independent': 'bg-party-independent'
};

export function VoteBreakdown({ votes }: VoteBreakdownProps) {
  const totalVotes = votes.reduce((sum, v) => sum + v.yea + v.nay + v.abstain, 0);

  return (
    <div className="space-y-3">
      <h4 className="text-sm font-medium text-foreground">Vote Breakdown by Party</h4>
      
      {/* Stacked Bar */}
      <div className="flex h-6 w-full overflow-hidden rounded-full bg-muted">
        {votes.map(vote => {
          const yeaPercent = (vote.yea / totalVotes) * 100;
          return yeaPercent > 0 ? (
            <div
              key={vote.party}
              className={cn('transition-all', partyColors[vote.party])}
              style={{ width: `${yeaPercent}%` }}
              title={`${vote.party}: ${vote.yea} Yea`}
            />
          ) : null;
        })}
      </div>

      {/* Party Details */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
        {votes.map(vote => (
          <div key={vote.party} className="flex items-center justify-between gap-2 p-2 rounded-md bg-muted/50">
            <div className="flex items-center gap-2">
              <div className={cn('h-3 w-3 rounded-full', partyColors[vote.party])} />
              <span className="font-medium">{vote.party}</span>
            </div>
            <div className="flex gap-3 text-muted-foreground">
              <span className="text-success">Y: {vote.yea}</span>
              <span className="text-destructive">N: {vote.nay}</span>
              {vote.abstain > 0 && <span>A: {vote.abstain}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
