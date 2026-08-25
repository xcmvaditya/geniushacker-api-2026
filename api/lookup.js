// GENIUS HACKER 29 API - Node.js Version

export default async function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    try {
        // Get mobile number from query
        const { mobile } = req.query;

        // If no mobile parameter
        if (!mobile) {
            return res.status(400).json({
                status: false,
                error: 'Mobile number required',
                usage: '/api/lookup?mobile=9876543210'
            });
        }

        // Validate mobile number
        if (!/^\d{10}$/.test(mobile)) {
            return res.status(400).json({
                status: false,
                error: 'Invalid mobile number',
                message: 'Please send exactly 10 digits'
            });
        }

        // Call the original API
        const originalUrl = `https://ethicaltabbo.in/api/lookup?key=Sahil&mobile=${mobile}`;
        
        const response = await fetch(originalUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            return res.status(500).json({
                status: false,
                error: 'Original API returned error',
                code: response.status
            });
        }

        const data = await response.json();

        // Clean the data - remove unwanted fields
        const unwantedFields = ['telegram', 'channel', 'credit', 'api_info'];
        unwantedFields.forEach(field => {
            if (data[field]) delete data[field];
        });

        // Remove unwanted fields from records
        if (data.data && Array.isArray(data.data)) {
            data.data = data.data.map(record => {
                const cleanRecord = { ...record };
                delete cleanRecord.id;
                delete cleanRecord.alt_number;
                return cleanRecord;
            });
        }

        // Add your branding
        data.credit = 'GENIUS HACKER 29 API';
        data.developer = 'ADIBHAI';
        data.youtube = 'https://youtube.com/@geniushacker29';

        // Send success response
        return res.status(200).json(data);

    } catch (error) {
        console.error('API Error:', error);
        
        // Handle specific errors
        if (error.message.includes('fetch')) {
            return res.status(503).json({
                status: false,
                error: 'Connection error - API unreachable'
            });
        }

        if (error.message.includes('timeout')) {
            return res.status(504).json({
                status: false,
                error: 'Request timeout - please try again'
            });
        }

        return res.status(500).json({
            status: false,
            error: 'Internal server error',
            message: error.message
        });
    }
}
