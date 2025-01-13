function filterMaxTimestampByDateAndUser() {
  const spreadsheetId = "1PwDUAK_xoLEpQ4-iulutSS29J9qtC7X1PwxwrVra9FU"; // Replace with your spreadsheet ID
  const sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();

  // Get all data from the sheet
  const data = sheet.getDataRange().getValues();

  if (data.length <= 1) {
    Logger.log("No data to process.");
    return;
  }

  // Extract headers and rows
  const headers = data[0]; // First row as headers
  const rows = data.slice(1); // Remaining rows as data

  // Find indexes of relevant columns
  const usernameIndex = headers.indexOf("username");
  const timestampIndex = headers.indexOf("Timestamp");

  if (usernameIndex === -1 || timestampIndex === -1) {
    throw new Error("Required columns 'username' or 'Timestamp' not found.");
  }

  // Group by date (first 10 digits of the timestamp) and username
  const groupedData = rows.reduce((acc, row) => {
    const timestamp = row[timestampIndex];
    if (!timestamp) return acc; // Skip rows with no timestamp

    const date = timestamp.toString().slice(0, 10); // First 10 digits as date
    const username = row[usernameIndex];

    // Create a unique key for grouping by date and username
    const groupKey = `${date}_${username}`;

    // Compare the current row's timestamp to the stored one and keep the latest
    if (!acc[groupKey] || new Date(row[timestampIndex]) > new Date(acc[groupKey][timestampIndex])) {
      acc[groupKey] = row;
    }

    return acc;
  }, {});

  // Extract rows to keep
  const rowsToKeep = Object.values(groupedData);

  // Clear the sheet and write back headers and filtered data
  sheet.clear(); // Clears the sheet
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]); // Write headers
  sheet.getRange(2, 1, rowsToKeep.length, headers.length).setValues(rowsToKeep); // Write filtered rows

  Logger.log("Sheet updated to keep only the max timestamp per date and user.");
}
