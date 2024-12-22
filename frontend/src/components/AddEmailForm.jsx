import React, {useState} from 'react';


const AddEmailForm = ({ addEmail: handleAddEmail }) => {
    const [email, setEmail] = useState('');

    const handleSubmit = () => {
        handleAddEmail(email); // Use the prop function to handle the email
        setEmail(''); // Reset the input field
    };

    return (
        <div>
            <input 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="Enter email" 
            />
            <button onClick={handleSubmit}>Add Email</button>
        </div>
    );
};

export default AddEmailForm;
