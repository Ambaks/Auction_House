import React, {useEffect, useState} from 'react';
import api from '../api.js';
import AddEmailForm from './AddEmailForm';



const EmailList = () => {
    const[email, setEmail] = useState([]);

    // Fetch emails on mount
    useEffect(() => {
        const fetchEmails = async () => {
            try {
                const response = await api.get('/email'); // Assuming API returns a list of emails
                setEmail(response.data);
            } catch (error) {
                console.error("Error fetching emails", error);
            }
        };

        fetchEmails();
    }, []);

    const addEmail = async (user_email) =>{
        try{
            await api.post('/email', {email: user_email});
        } catch (error){
            alert("Failed to add email. Please try again.")
            console.error("Error adding email", error)
        }
    };
    
    return (
        <div>
            <AddEmailForm addEmail={addEmail}/>
            <ul>
                {email.map((e, index) => (
                    <li key={index}>{e}</li>
                ))}
            </ul>
        </div>
    );
};

export default EmailList;