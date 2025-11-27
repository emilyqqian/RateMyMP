// Core data types for RateMyMP

export type PartyName = 'Liberal' | 'Conservative' | 'NDP' | 'Bloc Québécois' | 'Green' | 'Independent';

export type VoteStatus = 'Passed' | 'Failed' | 'In Progress';

export type MotionCategory = 
  | 'economics'
  | 'trade'
  | 'healthcare'
  | 'justice'
  | 'environment/energy'
  | 'social rights/Indigenous affairs'
  | 'foreign affairs'
  | 'immigration'
  | 'infrastructure';

export type MotionClassification = 'substantive' | 'subsidiary' | 'privileged' | 'incidental';

export interface PartyVote {
  party: PartyName;
  yea: number;
  nay: number;
  abstain: number;
}

export interface Motion {
  id: string;
  title: string;
  description: string;
  introducedBy: {
    mpId: string;
    mpName: string;
    party: PartyName;
  };
  status: VoteStatus;
  categories: MotionCategory[];
  classification: MotionClassification;
  voteBreakdown: PartyVote[];
  date: string;
  upvotes: number;
  downvotes: number;
  userVote?: 'up' | 'down';
}

export interface MP {
  id: string;
  name: string;
  riding: string;
  party: PartyName;
  imageUrl?: string;
  attendanceRate: number;
  partyLineVoting: number;
  yearsInOffice: number;
  email?: string;
  constituencyOffice?: string;
  socialMedia?: {
    twitter?: string;
    facebook?: string;
    website?: string;
  };
}

export interface Vote {
  id: string;
  motionTitle: string;
  vote: 'Yea' | 'Nay' | 'Abstain';
  date: string;
  matchedPartyLine: boolean;
  proposedByParty: PartyName;
  motionPassed: boolean;
  motionId: string;
}

export interface Speech {
  id: string;
  date: string;
  topic: string;
  excerpt: string;
  fullText: string;
  wordCount: number;
}

export interface SpendingItem {
  category: string;
  amount: number;
  percentage: number;
}

export interface TransparencyItem {
  type: 'stock' | 'conflict' | 'gift' | 'travel';
  description: string;
  date: string;
  value?: string;
}
