import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { MPHeader } from '@/components/MPHeader';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { MP } from '@/types';

// Mock data - will be replaced with API calls
const mockMP: MP = {
  id: 'mp1',
  name: 'John Smith',
  riding: 'Toronto Centre',
  party: 'Liberal',
  attendanceRate: 94,
  partyLineVoting: 87,
  yearsInOffice: 6,
  email: 'john.smith@parl.gc.ca',
  constituencyOffice: '123 Parliament St, Toronto, ON M5A 1A1',
  socialMedia: {
    twitter: '@johnsmith',
    website: 'johnsmith.ca'
  }
};

export default function MPProfile() {
  const { mpId } = useParams<{ mpId: string }>();
  const [mp] = useState<MP>(mockMP);

  return (
    <div className="min-h-screen bg-background">
      <div className="container py-8 space-y-6">
        <MPHeader mp={mp} />

        <Tabs defaultValue="voting" className="w-full">
          <TabsList className="grid w-full grid-cols-2 lg:grid-cols-5">
            <TabsTrigger value="voting">Voting Record</TabsTrigger>
            <TabsTrigger value="activity">Activity</TabsTrigger>
            <TabsTrigger value="spending">Spending</TabsTrigger>
            <TabsTrigger value="transparency">Transparency</TabsTrigger>
            <TabsTrigger value="contact">Contact</TabsTrigger>
          </TabsList>

          <TabsContent value="voting" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="font-display">Recent Votes</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Voting record data will be displayed here</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="activity" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="font-display">Parliamentary Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Speeches and attendance data will be displayed here</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="spending" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="font-display">Spending Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Budget usage and spending data will be displayed here</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="transparency" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="font-display">Transparency Information</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">Ethics registrar data will be displayed here</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="contact" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="font-display">Contact Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="font-medium text-sm text-muted-foreground mb-1">Email</div>
                  <div className="text-foreground">{mp.email}</div>
                </div>
                <div>
                  <div className="font-medium text-sm text-muted-foreground mb-1">Constituency Office</div>
                  <div className="text-foreground">{mp.constituencyOffice}</div>
                </div>
                {mp.socialMedia && (
                  <div>
                    <div className="font-medium text-sm text-muted-foreground mb-1">Social Media</div>
                    <div className="space-y-1">
                      {mp.socialMedia.twitter && (
                        <div className="text-foreground">{mp.socialMedia.twitter}</div>
                      )}
                      {mp.socialMedia.website && (
                        <div className="text-foreground">{mp.socialMedia.website}</div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
