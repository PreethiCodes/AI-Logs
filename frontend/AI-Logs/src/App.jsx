import ChatWindow from "./components/ChatWindow";
import MetricsDashboard from "./components/MetricsDashboard";
import FailureDashboard from "./components/FailureDashboard";
import PriorityPanel from "./components/PriorityPanel";

function App() {
  return (
    <div>
      <h1>Ops AI Monitoring Dashboard</h1>

      <ChatWindow />
      <MetricsDashboard />
      <FailureDashboard />
      <PriorityPanel />
    </div>
  );
}

export default App;
