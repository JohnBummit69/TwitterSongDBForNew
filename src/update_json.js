//Function to auto update JSON
function uploadToGitHub() {
    const spreadsheetId = "Yourspreadsheet id"; // Replace with your spreadsheet ID
    const spreadsheet = SpreadsheetApp.openById(spreadsheetId);
    const sheet = spreadsheet.getActiveSheet();
    
    if (!sheet) {
        throw new Error("No active sheet found.");
    }

    const data = sheet.getDataRange().getValues();
    const jsonData = JSON.stringify(data);

    const GITHUB_USERNAME = "JohnBummit";
    const GITHUB_REPO = "Twitter_Song_DB";
    const FILE_NAME = "music_data.json"; // Name of the file to create/update in the repo
    const GITHUB_TOKEN = "your github token";

    const url = `https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/contents/${FILE_NAME}`;
    const headers = {
        Authorization: `token ${GITHUB_TOKEN}`
    };

    let sha = null;

    try {
        // Step 1: Check if the file exists and retrieve its SHA
        const getResponse = UrlFetchApp.fetch(url, { method: "GET", headers: headers });
        const fileData = JSON.parse(getResponse.getContentText());
        sha = fileData.sha; // Retrieve the SHA of the existing file
        Logger.log(`File exists. SHA: ${sha}`);
    } catch (e) {
        if (e.message.includes("404")) {
            Logger.log("File does not exist. It will be created.");
        } else {
            throw e; // If the error isn't a 404, rethrow it
        }
    }

    // Step 2: Create or update the file
    const payload = {
        message: sha ? "Update data from Google Sheets" : "Create data from Google Sheets",
        content: Utilities.base64Encode(jsonData),
        sha: sha // Include SHA only if updating an existing file
    };

    const options = {
        method: "PUT",
        headers: headers,
        payload: JSON.stringify(payload)
    };

    const response = UrlFetchApp.fetch(url, options);
    Logger.log(`Response: ${response.getContentText()}`);
}
