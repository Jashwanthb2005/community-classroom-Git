import React, { useState } from 'react';
import axios from 'axios';
import './Api.css';

function Api() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await axios.post('http://127.0.0.1:3000/api/predict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error uploading image:', error);
        }
    };

    return (
        <div className='main'>
            <h1 className='main-heading'>Plant Disease Detector</h1>

            <form onSubmit={handleSubmit} className='form'>
                <input type="file" className='choose' onChange={handleFileChange} /><br/>
                <br/>
                <button type="submit" className='upload'>Upload</button>
            </form>

            {result && (
                <div className='container result'>
                    <div className='row'>
                    <h2 className='prediction-result col col-12'>Prediction Result</h2>
                    
                    <div className='col-6 div'>
                        <p className='disease'>Disease:</p>
                        <p className='disease-des'> {result.title}</p>
                    </div>
                    <div className='col-6 image-div'>
                         <img className='image' src={result.image_url} alt="Disease" />
                    </div>
                    <div className='col-12 div'>
                        <p className='disease'>Description:</p> 
                        <p className='disease-des'>{result.description}</p>
                    </div>
                    <div className='col-12 div'>
                        <p className='disease'>Prevention:</p> 
                        <p className='disease-des'>{result.prevent}</p>
                    </div>
                    
                    <div className='col-12 div'>
                        <h3 className='supplement disease'>Supplement Information</h3>
                        <p className='disease-des'><strong>Supplement:</strong> {result.supplement_name}</p>
                    </div>
                    <div className='col-12 div'>
                        <img className='supplement-image'src={result.supplement_image_url} alt="Supplement" />
                        <a href={result.supplement_buy_link}>Buy Supplement</a>
                    </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Api;
