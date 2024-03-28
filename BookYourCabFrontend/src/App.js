import logo from './logo.svg';
import './App.css';
import CabList from './components/Cablist';
import BookingForm from './components/BookingPage';

export const BACKEND_URL = "https://cab-system-q95w.onrender.com/api/"


function App() {
  return (
    <div className="App">
      {/* <CabList /> */}
      <BookingForm />
    </div>
  );
}

export default App;
