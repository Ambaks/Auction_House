import React from 'react';
import './App.css';
import EmailList from './components/emails';

const App = () => {
  return (
    <div className='App'>
      <header className='App-header'>
        <h1>Anaia's Website</h1>
      </header>
      <main>
        <EmailList />
      </main>
      <ul>
        {email.map((e, index) => (
          <li key={index}>{e}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;