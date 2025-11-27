import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBar } from '@/components/SearchBar';
import { MotionCard } from '@/components/MotionCard';
import { TagFilter } from '@/components/TagFilter';
import type { Motion, MotionCategory } from '@/types';
import { getMotions, voteOnMotion } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

export default function Home() {
  const [motions, setMotions] = useState<Motion[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<MotionCategory | undefined>();
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    loadMotions();
  }, [selectedCategory]);

  const loadMotions = async () => {
    try {
      setLoading(true);
      const data = await getMotions(selectedCategory ? { category: selectedCategory } : undefined);
      setMotions(data);
    } catch (error) {
      toast({
        title: 'Error loading motions',
        description: 'Please try again later',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query: string, type: 'name' | 'postal') => {
    // Navigate to MP search/results page
    navigate(`/mp/search?q=${encodeURIComponent(query)}&type=${type}`);
  };

  const handleVote = async (motionId: string, vote: 'up' | 'down') => {
    try {
      await voteOnMotion(motionId, vote);
      toast({
        title: 'Vote recorded',
        description: 'Thank you for your feedback'
      });
    } catch (error) {
      toast({
        title: 'Error recording vote',
        variant: 'destructive'
      });
    }
  };

  const handleInfoClick = (motionId: string) => {
    // TODO: Open AI explanation modal/sidebar
    toast({
      title: 'AI Explanation',
      description: 'Coming soon - AI-powered motion analysis'
    });
  };

  const allCategories: MotionCategory[] = [
    'economics',
    'trade',
    'healthcare',
    'justice',
    'environment/energy',
    'social rights/Indigenous affairs',
    'foreign affairs',
    'immigration',
    'infrastructure'
  ];

  return (
    <div className="min-h-screen bg-background">
      <div className="container py-8 space-y-8">
        {/* Hero Section */}
        <div className="text-center space-y-4 py-8">
          <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground">
            Hold Your <span className="text-accent-red">Representatives</span> Accountable
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Track parliamentary votes, review MP performance, and stay informed about Canadian politics
          </p>
        </div>

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} />

        {/* Category Filters */}
        <div className="space-y-3">
          <h2 className="font-display text-xl font-semibold text-foreground">
            Filter by Category
          </h2>
          <TagFilter
            categories={allCategories}
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
          />
        </div>

        {/* Motions List */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-display text-2xl font-semibold text-foreground">
              Recent Parliamentary Motions
            </h2>
            <span className="text-sm text-muted-foreground">
              {motions.length} motion{motions.length !== 1 ? 's' : ''}
            </span>
          </div>

          {loading ? (
            <div className="text-center py-12 text-muted-foreground">
              Loading motions...
            </div>
          ) : motions.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              No motions found for this category
            </div>
          ) : (
            <div className="space-y-4">
              {motions.map(motion => (
                <MotionCard
                  key={motion.id}
                  motion={motion}
                  onVote={handleVote}
                  onInfoClick={handleInfoClick}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
