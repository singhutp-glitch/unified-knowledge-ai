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
                    console.log("sync-job-id",syncJob);
                    const response = await getSyncStatus(syncJob.sync_job_id)
    
                    if (cancelled) return;
    
                    const job = response;
    
                    setSyncJob(job);
    
                    const terminalStatuses = [
                        "completed",
                        "completed_with_errors",
                        "failed",
                        "cancelled"
                    ];
                    console.log("match - ",terminalStatuses.includes(job.status));

                    if (terminalStatuses.includes(job.status)) {
                        console.log("job completed");
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