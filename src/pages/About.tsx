import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function About() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container py-12 space-y-8 max-w-4xl">
        <div className="text-center space-y-4">
          <h1 className="font-display text-4xl font-bold text-foreground">
            About <span className="text-accent-red">RateMyMP</span>
          </h1>
          <p className="text-lg text-muted-foreground">
            Bringing transparency and accountability to Canadian politics
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">Our Mission</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-muted-foreground">
            <p>
              RateMyMP is a public accountability dashboard designed to help Canadians stay informed 
              about their elected representatives in Parliament. We believe that transparency is 
              fundamental to a healthy democracy.
            </p>
            <p>
              Our platform aggregates public data from official government sources including the 
              Open Parliament API, Parliament of Canada voting records, and ethics registrar 
              information to provide you with a comprehensive view of MP activity and performance.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">What We Track</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <h3 className="font-medium text-foreground">Parliamentary Votes</h3>
              <p className="text-sm text-muted-foreground">
                Track how MPs vote on bills and motions, including party-line voting patterns
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-medium text-foreground">Attendance & Activity</h3>
              <p className="text-sm text-muted-foreground">
                Monitor parliamentary attendance rates and participation in debates
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-medium text-foreground">Spending</h3>
              <p className="text-sm text-muted-foreground">
                Review how MPs use their budgets for office operations and staff
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-medium text-foreground">Transparency</h3>
              <p className="text-sm text-muted-foreground">
                Access information about conflicts of interest, gifts, and sponsored travel
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">Data Sources</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>All data is sourced from official public records:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Open Parliament API (openparliament.ca)</li>
              <li>House of Commons Voting Records</li>
              <li>Parliamentary Bills Database</li>
              <li>MP Expenditure Disclosures</li>
              <li>Ethics Commissioner Registry</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
