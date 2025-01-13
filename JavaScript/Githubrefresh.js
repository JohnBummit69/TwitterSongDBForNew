// Function to auto update JSON
function uploadToGitHub() {
    const spreadsheetId = "1PwDUAK_xoLEpQ4-iulutSS29J9qtC7X1PwxwrVra9FU"; // Replace with your spreadsheet ID
    const spreadsheet = SpreadsheetApp.openById(spreadsheetId);
    const sheet = spreadsheet.getActiveSheet();
    
    if (!sheet) {
        throw new Error("No active sheet found.");
    }

    const data = sheet.getDataRange().getValues();
    data[0] = ["Timestamp", "username", "song_name", "artist_name"];

    const data4 = data.map(row => row.slice(0, 4));
    const jsonData = convertToDict(data);
    const jsonString = JSON.stringify(jsonData);

    const GITHUB_USERNAME = "JohnBummit69";
    const GITHUB_REPO = "TwitterSongDB";
    const FILE_NAME = "src/music_data.json";
    const FILE_NAME2 = "App/src/music_datacloud.json";

    const urls = [
        `https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/contents/${FILE_NAME}`,
        `https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/contents/${FILE_NAME2}`
    ];

    const GITHUB_TOKEN = "github_token";
    const headers = {
        Authorization: `Bearer ${GITHUB_TOKEN}`
    };

    urls.forEach(url => {
        let sha = null;

        try {
            const getResponse = UrlFetchApp.fetch(url, { method: "GET", headers: headers });
            const fileData = JSON.parse(getResponse.getContentText());
            sha = fileData.sha;
            Logger.log(`File exists. SHA: ${sha}`);
        } catch (e) {
            if (e.message.includes("404")) {
                Logger.log("File does not exist. It will be created.");
            } else {
                throw e;
            }
        }

        const payload = {
            message: sha ? "Update data from Google Sheets" : "Create data from Google Sheets",
            content: Utilities.base64Encode(jsonString),
            sha: sha
        };

        const options = {
            method: "PUT",
            headers: headers,
            payload: JSON.stringify(payload)
        };

        const response = UrlFetchApp.fetch(url, options);
        Logger.log(`Response: ${response.getContentText()}`);
    });
}
