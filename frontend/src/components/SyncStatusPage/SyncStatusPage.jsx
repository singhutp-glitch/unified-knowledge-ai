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
                    console.log("status requested");
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
    
        }, [syncJob?.sync_job_id]);
 const progress = syncJob && syncJob.total_files > 0
    ? Math.min(
        (syncJob.completed_files / syncJob.total_files) * 100,
        100
      )
    : 0;

return (
    <div className="sync-status-page">

        {syncJob ? (

            <div className="sync-status-content">
                    <h2>Synchronization Status</h2>


                <div className="sync-status-info">

                    <div className="sync-status-label">
                        Current Status
                    </div>

                    <div className={`sync-status-value status-${syncJob.status}`}>
                        {syncJob.status.replaceAll("_", " ")}
                    </div>

                </div>

                <div className="sync-progress-section">

                    <div className="sync-progress-heading">

                        <span>Progress</span>

                        <span>
                            {syncJob.completed_files} / {syncJob.total_files} completed
                        </span>

                    </div>

                    <div className="sync-progress-bar">

                        <div
                            className="sync-progress-fill"
                            style={{ width: `${progress}%` }}
                        />

                    </div>

                    <div className="sync-progress-percentage">
                        {Math.round(progress)}%
                    </div>

                </div>

            </div>

        ) : (

            <div className="sync-status-empty">
                <p>No synchronization yet</p>
                <span>
                    Run a synchronization from the Checkout section
                    to see its progress here.
                </span>
            </div>

        )}

    </div>
);
}

export default SyncStatusPage