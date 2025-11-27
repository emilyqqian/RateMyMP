// API service layer - placeholder functions for backend integration
import type { Motion, MP, Vote, Speech, SpendingItem, TransparencyItem } from '@/types';

const API_BASE = '/api'; // Will be replaced with actual backend URL

// Mock data for development
export const mockMotions: Motion[] = [
  {
    id: '1',
    title: 'Bill C-15: An Act to amend the Canada Health Act',
    description: 'Amendment to expand coverage for mental health services',
    introducedBy: {
      mpId: 'mp1',
      mpName: 'John Smith',
      party: 'Liberal'
    },
    status: 'Passed',
    categories: ['healthcare'],
    classification: 'substantive',
    voteBreakdown: [
      { party: 'Liberal', yea: 155, nay: 0, abstain: 3 },
      { party: 'Conservative', yea: 25, nay: 94, abstain: 0 },
      { party: 'NDP', yea: 24, nay: 0, abstain: 1 },
      { party: 'Bloc Québécois', yea: 32, nay: 0, abstain: 0 },
      { party: 'Green', yea: 2, nay: 0, abstain: 0 }
    ],
    date: '2024-11-15',
    upvotes: 1247,
    downvotes: 342
  },
  {
    id: '2',
    title: 'Motion M-47: Climate Emergency Response Fund',
    description: 'Establish a $10B fund for climate adaptation infrastructure',
    introducedBy: {
      mpId: 'mp2',
      mpName: 'Marie Leclerc',
      party: 'NDP'
    },
    status: 'In Progress',
    categories: ['environment/energy', 'infrastructure'],
    classification: 'substantive',
    voteBreakdown: [
      { party: 'Liberal', yea: 120, nay: 38, abstain: 0 },
      { party: 'Conservative', yea: 0, nay: 119, abstain: 0 },
      { party: 'NDP', yea: 25, nay: 0, abstain: 0 },
      { party: 'Bloc Québécois', yea: 32, nay: 0, abstain: 0 },
      { party: 'Green', yea: 2, nay: 0, abstain: 0 }
    ],
    date: '2024-11-20',
    upvotes: 2156,
    downvotes: 891
  }
];

// Motions API
export async function getMotions(filters?: { category?: string }): Promise<Motion[]> {
  // TODO: Replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 300));
  
  if (filters?.category) {
    return mockMotions.filter(m => m.categories.includes(filters.category as any));
  }
  return mockMotions;
}

export async function getMotionById(id: string): Promise<Motion | null> {
  await new Promise(resolve => setTimeout(resolve, 200));
  return mockMotions.find(m => m.id === id) || null;
}

export async function voteOnMotion(motionId: string, vote: 'up' | 'down'): Promise<void> {
  // TODO: POST /api/motions/{id}/vote
  await new Promise(resolve => setTimeout(resolve, 100));
}

// MPs API
export async function searchMPs(query: string): Promise<MP[]> {
  // TODO: GET /api/mps?search={query}
  await new Promise(resolve => setTimeout(resolve, 300));
  return [];
}

export async function getMPByPostalCode(postalCode: string): Promise<MP | null> {
  // TODO: GET /api/lookup/postal-code/{code}
  await new Promise(resolve => setTimeout(resolve, 300));
  return null;
}

export async function getMPById(id: string): Promise<MP | null> {
  // TODO: GET /api/mps/{id}
  await new Promise(resolve => setTimeout(resolve, 300));
  return null;
}

export async function getMPVotes(mpId: string): Promise<Vote[]> {
  // TODO: GET /api/mps/{id}/votes
  await new Promise(resolve => setTimeout(resolve, 300));
  return [];
}

export async function getMPSpeeches(mpId: string): Promise<Speech[]> {
  // TODO: GET /api/mps/{id}/speeches
  await new Promise(resolve => setTimeout(resolve, 300));
  return [];
}

export async function getMPSpending(mpId: string): Promise<SpendingItem[]> {
  // TODO: GET /api/mps/{id}/spending
  await new Promise(resolve => setTimeout(resolve, 300));
  return [];
}

export async function getMPTransparency(mpId: string): Promise<TransparencyItem[]> {
  // TODO: GET /api/mps/{id}/transparency
  await new Promise(resolve => setTimeout(resolve, 300));
  return [];
}
