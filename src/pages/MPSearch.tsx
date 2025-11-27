import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { searchMPs, getMPByPostalCode } from '@/services/api';
import type { MP, PartyName } from '@/types';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

const partyColors: Record<PartyName, string> = {
  'Liberal': 'bg-party-liberal text-white',
  'Conservative': 'bg-party-conservative text-white',
  'NDP': 'bg-party-ndp text-white',
  'Bloc Québécois': 'bg-party-bloc text-white',
  'Green': 'bg-party-green text-white',
  'Independent': 'bg-party-independent text-white'
};

export default function MPSearch() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState<MP[]>([]);

  const query = searchParams.get('q') || '';
  const type = searchParams.get('type') as 'name' | 'postal';

  useEffect(() => {
    performSearch();
  }, [query, type]);

  const performSearch = async () => {
    try {
      setLoading(true);
      if (type === 'postal') {
        const mp = await getMPByPostalCode(query);
        setResults(mp ? [mp] : []);
      } else {
        const mps = await searchMPs(query);
        setResults(mps);
      }
    } catch (error) {
      toast({
        title: 'Search failed',
        description: 'Please try again',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container py-8 space-y-6">
        <div>
          <h1 className="font-display text-3xl font-bold text-foreground mb-2">
            Search Results
          </h1>
          <p className="text-muted-foreground">
            {type === 'postal' 
              ? `Looking up MP for postal code: ${query}`
              : `Searching for MPs matching: ${query}`
            }
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12 text-muted-foreground">
            Searching...
          </div>
        ) : results.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground mb-4">
                No MPs found matching your search
              </p>
              <Button onClick={() => navigate('/')}>
                Back to Home
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {results.map(mp => (
              <Card
                key={mp.id}
                className="cursor-pointer hover:shadow-lg transition-shadow border-card-border"
                onClick={() => navigate(`/mp/${mp.id}`)}
              >
                <CardHeader>
                  <div className="flex items-start gap-4">
                    {mp.imageUrl ? (
                      <img
                        src={mp.imageUrl}
                        alt={mp.name}
                        className="w-16 h-16 rounded-lg object-cover border-2 border-border"
                      />
                    ) : (
                      <div className="w-16 h-16 rounded-lg bg-muted flex items-center justify-center border-2 border-border">
                        <span className="text-xl font-display font-bold text-muted-foreground">
                          {mp.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-display font-semibold text-foreground truncate">
                        {mp.name}
                      </h3>
                      <p className="text-sm text-muted-foreground">{mp.riding}</p>
                      <Badge className={cn('mt-2 text-xs', partyColors[mp.party])}>
                        {mp.party}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      <div className="text-muted-foreground">Attendance</div>
                      <div className="font-medium">{mp.attendanceRate}%</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">Party Line</div>
                      <div className="font-medium">{mp.partyLineVoting}%</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
