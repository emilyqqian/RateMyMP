import { Badge } from '@/components/ui/badge';
import type { MotionCategory } from '@/types';
import { cn } from '@/lib/utils';

interface TagFilterProps {
  categories: MotionCategory[];
  selectedCategory?: MotionCategory;
  onSelectCategory: (category?: MotionCategory) => void;
}

const categoryLabels: Record<MotionCategory, string> = {
  'economics': 'Economics',
  'trade': 'Trade',
  'healthcare': 'Healthcare',
  'justice': 'Justice',
  'environment/energy': 'Environment & Energy',
  'social rights/Indigenous affairs': 'Social Rights & Indigenous',
  'foreign affairs': 'Foreign Affairs',
  'immigration': 'Immigration',
  'infrastructure': 'Infrastructure'
};

export function TagFilter({ categories, selectedCategory, onSelectCategory }: TagFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <Badge
        variant={!selectedCategory ? 'default' : 'outline'}
        className={cn(
          'cursor-pointer transition-colors',
          !selectedCategory ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'
        )}
        onClick={() => onSelectCategory(undefined)}
      >
        All Categories
      </Badge>
      
      {categories.map(cat => (
        <Badge
          key={cat}
          variant={selectedCategory === cat ? 'default' : 'outline'}
          className={cn(
            'cursor-pointer transition-colors',
            selectedCategory === cat ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'
          )}
          onClick={() => onSelectCategory(cat)}
        >
          {categoryLabels[cat]}
        </Badge>
      ))}
    </div>
  );
}
