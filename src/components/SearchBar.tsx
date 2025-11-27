import { useState } from 'react';
import { Search, MapPin } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface SearchBarProps {
  onSearch: (query: string, type: 'name' | 'postal') => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [searchType, setSearchType] = useState<'name' | 'postal'>('name');
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), searchType);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-3">
      <Tabs value={searchType} onValueChange={(v) => setSearchType(v as 'name' | 'postal')}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="name" className="gap-2">
            <Search className="h-4 w-4" />
            MP Name
          </TabsTrigger>
          <TabsTrigger value="postal" className="gap-2">
            <MapPin className="h-4 w-4" />
            Postal Code
          </TabsTrigger>
        </TabsList>
      </Tabs>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          type="text"
          placeholder={
            searchType === 'name'
              ? 'Search by MP name...'
              : 'Enter your postal code (e.g., K1A 0A6)...'
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1"
        />
        <Button type="submit" size="default" className="bg-primary hover:bg-primary-hover">
          Search
        </Button>
      </form>
    </div>
  );
}
