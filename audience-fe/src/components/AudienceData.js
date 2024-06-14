import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);


const AudienceData = () => {
    const [stats, setStats] = useState({});
    const [chartData, setChartData] = useState({ labels: [], datasets: [] });
    const [file, setFile] = useState(null)
    const [fileId, setFileId] = useState(null)

    // handles if we are changing the file we want displayed
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    }
    
    // handles uploading the file we want to display the statistics of
    const handleFileUpload = () => {
        if (!file) {
            console.error("No file selected");
            return;
        }
        const formData = new FormData();
        formData.append('file', file);

        // post method to integrate the file upload method with the Backend post method
        axios.post('http://localhost:8000/api/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        // either upload the file successfully or catch the error
        .then(response => {
            console.log('File uploaded successfully:', response.data);
            setFileId(response.data.id);
        })
        .catch(error => {
            console.error('Error encountered while uploading file:', error)
        });
    };

    useEffect(() => {
        // if we have a valid file, get the file from the Backend
        if (fileId) {
            axios.get(`http://localhost:8000/api/get_stats/${fileId}/`)
            .then(response=> {
                console.log('Response Data:', response.data);
                setStats(response.data);

                const labels = response.data.labels || [];
                const data = response.data.data || [];

                console.log('Labels:', labels);
                console.log('Data:', data);

                // check that the number of labels and number of data entries are the same
                // so the data can be displayed correctly and neatly on the chart;
                // otherwise, display the dataset information and populate the graph/chart accordingly
                if (labels.length !== data.length) {
                    console.error('Labels and data length mismatch');
                } else {
                    setChartData({
                        labels,
                        datasets: [
                            {
                                label: 'Efficiency vs Reach',
                                data: data,
                                backgroundColor: 'rgba(75, 190, 190, 0.5)',
                                borderColor: 'rgba(75, 190, 190, 1)',
                                borderWidth: 1,
                            },
                        ],
                    });
                }
            })
            // catch any other errors not specifically accounted for previously
            .catch(error => {
                console.error('Error with stats fetch: ', error)
            });
        }
    }, [fileId]);

    return (
        <div>
            <h1>Key Statistics</h1>
            {/* File Upload Form */}
            <div>
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleFileUpload}>Upload File</button>
            </div>
            {/* Display Stats */}
            <div>
                <p>Zipcode: {stats.zipcode_number}</p>
                <p>Audience Reach: {stats.audience_reach}</p>
                <p>Total Reach: {stats.total_reach}</p>
                <p>Percentage Reach: {stats.pct_reach}</p>
                <p>Target Density: {stats.target_density}</p>
            </div>
            {/* Chart */}
            <Line data={ chartData } />
        </div>
    );
};

export default AudienceData;
