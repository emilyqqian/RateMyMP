import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import type { MP, PartyName } from '@/types';
import { cn } from '@/lib/utils';

interface MPHeaderProps {
  mp: MP;
}

const partyColors: Record<PartyName, string> = {
  'Liberal': 'bg-party-liberal text-white',
  'Conservative': 'bg-party-conservative text-white',
  'NDP': 'bg-party-ndp text-white',
  'Bloc Québécois': 'bg-party-bloc text-white',
  'Green': 'bg-party-green text-white',
  'Independent': 'bg-party-independent text-white'
};

export function MPHeader({ mp }: MPHeaderProps) {
  return (
    <Card className="border-card-border">
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row gap-6">
          {/* MP Photo */}
          <div className="flex-shrink-0">
            {mp.imageUrl ? (
              <img
                src={mp.imageUrl}
                alt={mp.name}
                className="w-32 h-32 rounded-lg object-cover border-2 border-border"
              />
            ) : (
              <div className="w-32 h-32 rounded-lg bg-muted flex items-center justify-center border-2 border-border">
                <span className="text-4xl font-display font-bold text-muted-foreground">
                  {mp.name.split(' ').map(n => n[0]).join('')}
                </span>
              </div>
            )}
          </div>

          {/* MP Info */}
          <div className="flex-1 space-y-4">
            <div>
              <h1 className="font-display text-3xl font-bold text-foreground mb-2">
                {mp.name}
              </h1>
              <div className="flex flex-wrap items-center gap-2">
                <Badge className={cn('text-sm', partyColors[mp.party])}>
                  {mp.party}
                </Badge>
                <span className="text-muted-foreground">•</span>
                <span className="text-muted-foreground">{mp.riding}</span>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div className="space-y-1">
                <div className="text-2xl font-display font-bold text-foreground">
                  {mp.attendanceRate}%
                </div>
                <div className="text-xs text-muted-foreground">Attendance Rate</div>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-display font-bold text-foreground">
                  {mp.partyLineVoting}%
                </div>
                <div className="text-xs text-muted-foreground">Party-Line Voting</div>
              </div>
              <div className="space-y-1">
                <div className="text-2xl font-display font-bold text-foreground">
                  {mp.yearsInOffice}
                </div>
                <div className="text-xs text-muted-foreground">Years in Office</div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
