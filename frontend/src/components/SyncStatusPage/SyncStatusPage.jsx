import {useEffect} from 'react'
import "./SyncStatusPage.css"
import { getSyncStatus } from '../../services/sourceApi';

const SyncStatusPage = ({syncJob,setSyncJob}) => {
    useEffect(() => {
    
            if (!syncJob) return;
    
            let cancelled = false;
            let timeoutId;
    
            async function fetchSyncStatus() {
    
                try {
                    const response = await getSyncStatus(syncJob.id)
    
                    if (cancelled) return;
    
                    const job = response.data;
    
                    setSyncJob(job);
    
                    const terminalStatuses = [
                        "completed",
                        "completed_with_errors",
                        "failed",
                        "cancelled"
                    ];
    
                    if (terminalStatuses.includes(job.status)) {
                        return;
                    }
    
                } catch (error) {
                    if (cancelled) return;
    
                    console.error(
                        "Failed to retrieve sync status:",
                        error
                    );
                }
    
                if (!cancelled) {
                    timeoutId = setTimeout(
                        fetchSyncStatus,
                        3000
                    );
                }
            }
    
            fetchSyncStatus();
    
            return () => {
                cancelled = true;
                clearTimeout(timeoutId);
            };
    
        }, []);
  return (
    <div className="sync-status-page">
          <h2>Synchronization Status</h2>

            {syncJob ? (
                <div>
                    <p>Status: {syncJob.status}</p>

                    <p>
                        Completed: {syncJob.completed_files}
                        / {syncJob.total_files}
                    </p>
                </div>
            ) : (
                <p>No synchronization yet</p>
            )}
        </div>
  )
}

export default SyncStatusPage