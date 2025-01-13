// Convert JSON array to dictionary-like objects
function convertToDict(data) {
    const headers = data[0]; // Extract the first row as keys
    const rows = data.slice(1); // Extract remaining rows as values

    // Map rows into an array of objects
    const dictArray = rows.map(row => {
        const obj = {};
        headers.forEach((key, index) => {
            obj[key] = row[index] || ""; // Use an empty string for missing values
        });
        return obj;
    });

    return dictArray;
}
