let pickerApiReady = false;
let pickerApiLoading = null;


function loadPickerApi() {
    if (pickerApiReady) {
        return Promise.resolve();
    }

    if (pickerApiLoading) {
        return pickerApiLoading;
    }

    pickerApiLoading = new Promise((resolve, reject) => {

        if (!window.gapi) {
            reject(
                new Error("Google API library has not loaded yet")
            );
            return;
        }

        window.gapi.load("picker", {
            callback: () => {
                pickerApiReady = true;
                resolve();
            },
            onerror: () => {
                reject(
                    new Error("Failed to load Google Picker API")
                );
            }
        });
    });

    return pickerApiLoading;
}


export async function openGoogleDrivePicker(
    accessToken,
    onFolderSelected
) {
    try {

        await loadPickerApi();

        const view = new google.picker.DocsView(
            google.picker.ViewId.DOCS
        );

        // Show folders in the Picker
        view.setIncludeFolders(true);

        // Allow the user to select a folder
        view.setSelectFolderEnabled(true);

        const picker = new google.picker.PickerBuilder()
            .setDeveloperKey(
                import.meta.env.VITE_GOOGLE_API_KEY
            )
            .setAppId(
                import.meta.env.VITE_GOOGLE_PROJECT_NUMBER
            )
            .setOAuthToken(accessToken)
            .addView(view)
            .setCallback((data) => {

                if (
                    data.action ===
                    google.picker.Action.PICKED
                ) {

                    const selectedDocument =
                        data[
                            google.picker.Response.DOCUMENTS
                        ][0];

                    const folderId =
                        selectedDocument[
                            google.picker.Document.ID
                        ];

                    const folderName =
                        selectedDocument[
                            google.picker.Document.NAME
                        ];

                    // Give the selected folder
                    // back to the React component
                    onFolderSelected({
                        id: folderId,
                        name: folderName
                    });
                }

                if (
                    data.action ===
                    google.picker.Action.CANCEL
                ) {
                    // User closed Picker
                }
            })
            .build();

        picker.setVisible(true);

    } catch (error) {
        console.error(
            "Google Drive Picker error:",
            error
        );
        throw error;
    }
}