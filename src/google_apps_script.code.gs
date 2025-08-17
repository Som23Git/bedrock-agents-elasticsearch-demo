function generateUberNDJSON() {
  const threads = GmailApp.search('from:(noreply@uber.com) subject:"trip with Uber"');
  let ndjsonLines = [];

  function extract(html, regex) {
    const match = html.match(regex);
    return match ? match[1].trim() : null;
  }

  function parseCurrency(str) {
    return str ? parseFloat(str.replace(/[₹,]/g, '')) : null;
  }

  function parseDistance(str) {
    return str ? parseFloat(str.replace(/[^\d.]/g, '')) : null;
  }

  function parseTimeTo24Hour(timeStr) {
    if (!timeStr) return null;
    const [time, ampm] = timeStr.split(' ');
    let [hours, minutes] = time.split(':').map(Number);
    if (ampm === 'PM' && hours < 12) hours += 12;
    if (ampm === 'AM' && hours === 12) hours = 0;
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
  }

  function parseDateISO(dateStr) {
    const d = new Date(dateStr);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function getISTDateTimeISO(dateStr, timeStr) {
    if (!dateStr || !timeStr) return null;
    const [hourStr, minStr] = timeStr.split(':');
    const d = new Date(dateStr);
    d.setHours(Number(hourStr), Number(minStr), 0, 0);
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:00+05:30`;
  }

  function getTripDateInWords(dateStr) {
  const d = new Date(dateStr);
  const day = d.getDate();
  const month = d.toLocaleString('default', { month: 'long' });
  const year = d.getFullYear();
  const suffix = (day) => {
    if (day >= 11 && day <= 13) return 'th';
    return {1: 'st', 2: 'nd', 3: 'rd'}[day % 10] || 'th';
  };
  return `${day}${suffix(day)} of ${month} ${year}`;
  }


  for (let thread of threads) {
    const msg = thread.getMessages()[0];
    const html = msg.getBody();
    const cleanText = html.replace(/<[^>]+>/g, '');

    const tripDateRaw = extract(html, /(\w+ \d{1,2}, \d{4})<\/span>/);
    const trip_date = parseDateISO(tripDateRaw);
    const driver = extract(html, /You rode with ([^<]+)</);
    const distance_km = parseDistance(extract(html, /([0-9.]+ kilometers)/));

    const timeLocRegex = /(\d{1,2}:\d{2} [AP]M).*?<td class="Uber18_text_p1 black"[^>]*>([^<]+)/g;
    const timeLocMatches = [...html.matchAll(timeLocRegex)];
    const pickup_time_raw = timeLocMatches[1]?.[1] || null;
    const pickup_time = parseTimeTo24Hour(pickup_time_raw);
    const pickup_location = timeLocMatches[1]?.[2] || null;
    const dropoff_time_raw = timeLocMatches[2]?.[1] || null;
    const dropoff_time = parseTimeTo24Hour(dropoff_time_raw);
    const dropoff_location = timeLocMatches[2]?.[2] || null;

    const pickup_timestamp = getISTDateTimeISO(trip_date, pickup_time);
    const dropoff_timestamp = getISTDateTimeISO(trip_date, dropoff_time);

    const tripChunk = cleanText.match(/Trip\s*Charge(.{0,50})/i);
    const tripChargeMatch = tripChunk ? tripChunk[1].match(/₹[\d.,]+/) : null;
    const promotionMatch = cleanText.match(/Promotion\s*-?₹[\d.,]+/i);
    const totalMatch = cleanText.match(/Total\s*₹[\d.,]+/i);

    const trip_charge_inr = parseCurrency(tripChargeMatch ? tripChargeMatch[0] : null);
    const promotion_inr = parseCurrency(promotionMatch ? promotionMatch[0].match(/-?₹[\d.,]+/)[0] : null);
    const total_fare_inr = parseCurrency(totalMatch ? totalMatch[0].match(/₹[\d.,]+/)[0] : null);

    let duration_minutes = null;
    if (pickup_time && dropoff_time) {
      const refDate = new Date(trip_date);
      const parseTime = (str) => {
        const [h, m] = str.split(':').map(Number);
        const d = new Date(refDate);
        d.setHours(h, m, 0, 0);
        return d;
      };
      const pickup = parseTime(pickup_time);
      const dropoff = parseTime(dropoff_time);
      duration_minutes = Math.round((dropoff - pickup) / (1000 * 60));
    }

    // const summary_text = `On ${trip_date}, you took an Uber ride from ${pickup_location} to ${dropoff_location}. The trip started at ${pickup_time} and ended at ${dropoff_time}, lasting ${duration_minutes} minutes and covering ${distance_km} kilometers. Your driver was ${driver}. The total fare was INR ${total_fare_inr} after a promotion of INR ${Math.abs(promotion_inr)} was applied to the original trip charge of INR ${trip_charge_inr}.`;
    
    const trip_date_words = getTripDateInWords(trip_date);
    let summary_text = `Trip taken on ${trip_date}. On ${trip_date_words}, you took an Uber ride from ${pickup_location} to ${dropoff_location}. `;
    summary_text += `The trip started at ${pickup_time} and ended at ${dropoff_time}, lasting ${duration_minutes} minutes and covering ${distance_km} kilometers. `;
    summary_text += `Your driver was ${driver}. `;
    summary_text += `The total fare was INR ${total_fare_inr}`;
    if (promotion_inr != null && trip_charge_inr != null) {
      summary_text += ` after a promotion of INR ${Math.abs(promotion_inr)} was applied to the original trip charge of INR ${trip_charge_inr}.`;
    } else {
      summary_text += ` with no promotion applied.`;
    };

    const doc = {
      trip_date,
      pickup_timestamp,
      dropoff_timestamp,
      pickup_location,
      dropoff_location,
      driver,
      distance_km,
      trip_charge_inr,
      promotion_inr,
      total_fare_inr,
      duration_minutes,
      summary_text
    };

    ndjsonLines.push(JSON.stringify(doc));
  }

  const ndjsonContent = ndjsonLines.join('\n');
  DriveApp.createFile('uber_trips.ndjson', ndjsonContent, MimeType.PLAIN_TEXT);
  Logger.log('✅ NDJSON file "uber_trips.ndjson" created in your Google Drive.');
}