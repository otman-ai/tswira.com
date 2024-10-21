import axios from 'axios';

export const getData = async (endpoint, token) => {
    try {
        const response = await axios.get(endpoint, {
            headers: {
                'Authorization': `Token ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // Rethrow the error for further handling
    }
};