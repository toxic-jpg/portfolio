# CF7 to Google Sheets

WordPress plugin that sends Contact Form 7 submissions directly to Google Sheets — no Zapier, no Make, no monthly fees.

## Setup (5 minutes)

1. **Create Google Apps Script Webhook:**
   - Go to [script.google.com](https://script.google.com)
   - New Project → paste `apps-script/Code.gs` (see below)
   - Deploy → New Deployment → Web App → Execute as: Me, Access: Anyone
   - Copy the webhook URL

2. **Install Plugin:**
   - Zip this folder → WP Admin → Plugins → Add New → Upload Plugin
   - Activate

3. **Configure:**
   - Go to Contact → CF7 → Google Sheets
   - Select your form, paste webhook URL
   - Map CF7 fields (your-name, your-email, etc.) to Sheet columns
   - Save

## Apps Script Code (`apps-script/Code.gs`)

```javascript
function doPost(e) {
  const sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getActiveSheet();
  const data = JSON.parse(e.postData.contents);
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  
  const row = headers.map(h => data[h] ?? '');
  sheet.appendRow(row);
  
  return ContentService.createTextOutput(JSON.stringify({success: true}))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Replace `YOUR_SHEET_ID` from your sheet URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`

## Features

- ✅ Zero dependencies (no Composer, no npm)
- ✅ Works with any CF7 form
- ✅ Field mapping UI in WP Admin
- ✅ Timestamp + Form ID auto-added
- ✅ Handles checkboxes, selects, file uploads (stores filenames)
- ✅ Fails silently — never blocks email sending

## Requirements

- WordPress 5.5+
- Contact Form 7 5.0+
- PHP 7.4+