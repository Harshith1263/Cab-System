import React, { useState,useEffect } from 'react';
import DatePicker from 'react-datepicker';
import { toast } from 'react-toastify';
import 'react-datepicker/dist/react-datepicker.css';
import Notification from './Notification';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import './BookingForm.css'; // Import your custom CSS file

const BookingForm = () => {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [email, setEmail] = useState('');
  const [dateTime, setDateTime] = useState('');
  const [selectedCab, setSelectedCab] = useState('');
  const [cabList, setCabList] = useState([]); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10
  const [estimatedTime, setEstimatedTime] = useState('');
  const [bookingStatus, setBookingStatus] = useState(null);
  const [estimatedCost, setEstimatedCost] = useState(0);
  const [selectedCabAvailability, setSelectedCabAvailability] = useState(null);
  const [locations, setLocations] = useState([]); // ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const bookingData = {
      source,
      destination,
      email,
      booking_time: dateTime.toISOString().slice(0, -5),
      required_cab: selectedCab
    };

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

    console.log('Booking data:', bookingData);
    console.log(JSON.stringify(bookingData))
    fetch(`http://localhost:8000/api/bookcab/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, 
      },
      body: JSON.stringify({"source":source,"destination":destination,"email":email,"booking_time":dateTime.toISOString(),"required_cab":selectedCab})
    })
    .then(response => {
      console.log("response",response)
      if (!response.ok) {
        throw new Error('Failed to book cab');
      }
      setBookingStatus('success');
      return response.json();
    })
    .then(data => {
      console.log('Booking successful:', data);
      alert('Cab booked successfully! Check your mail for further details..');
      fetchCabList()
      fetchLocations()
      setSource('');
      setDestination('');
      setEmail('');
      setDateTime('');
      setSelectedCab('');
    })
    .catch(error => {
      setBookingStatus('failure');
      console.error('Booking failed:', error.message);
      alert('Failed to book cab! Check the details and try again.');
    });
  };

  // useEffect(() => {
  //   if (bookingStatus === 'success') {
  //     toast.success('Cab booked successfully!');
  //   }else if (bookingStatus === 'failure') {
  //     toast.error('Failed to book cab!');
  //   }
  // }, [bookingStatus]);


  const fetchCabList = () => {
    fetch('http://localhost:8000/api/cablist/')
    .then(response => response.json())
    .then(data => {
      console.log('Cab list:', data);
      setCabList(data);
    }).catch(error => {
      console.error('Failed to fetch cab list:', error.message);
    });
  };

  useEffect(() => {
    if(source&&destination&&selectedCab){
      fetch(`http://localhost:8000/api/estimate-cost/${source}/${destination}/${selectedCab}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch estimated cost');
        }
        return response.json();
      })
      .then(data => {
        setEstimatedCost(data.estimated_cost);
      })
      .catch(error => {
        console.error('Error calculating estimated cost:', error);
        setEstimatedCost(null);
      });
    }else{
      setEstimatedCost(null)
    }
  },[source,destination,selectedCab])

  useEffect(() => {
    if (source && destination) {
      calculateEstimatedTime(source, destination);
    }else{
      setEstimatedTime(null);
    }
  }, [source, destination]);
  
  const calculateEstimatedTime = (source, destination) => {
    fetch(`http://localhost:8000/api/calc-estimated-time/${source}/${destination}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch estimated time');
        }
        return response.json();
      })
      .then(data => {
        setEstimatedTime(data.estimated_time);
      })
      .catch(error => {
        console.error('Error calculating estimated time:', error);
        setEstimatedTime(null);
      });
  };

  // useEffect(() => {
  //   if (selectedCab&&source&&destination&&dateTime&&!selectedCabAvailability) {
  //     handleCabAvailability();
  //   }else if(selectedCab){
  //     setSelectedCabAvailability(false)
  //   }else{
  //     setSelectedCabAvailability(null)
  //   }
  // }, [selectedCab, source, destination, dateTime]);

  const handleCabAvailability = () => {
    console.log('Checking cab availability:', source, destination, dateTime.toISOString().slice(0, -5), selectedCab);
    fetch(`http://localhost:8000/api/check-availability/${source}/${destination}/${dateTime.toISOString().slice(0, -5)}/${selectedCab}/`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch cab availability');
      }
      return response.json();
    })
    .then(data => {
      console.log('Cab availability:', data);
      setSelectedCabAvailability(data);
    })
    .catch(error => {
      console.error('Error checking cab availability:', error);
      setSelectedCabAvailability(false);
    });
  }


  useEffect(() => {
    fetchCabList();
    fetchLocations();
    console.log('locations',locations)
  }
  , []);

  const fetchLocations = () => {
    fetch('http://localhost:8000/api/get-locationnames/')
    .then(response => response.json())
    .then(data => {
      console.log('Locations:', data);
      setLocations(data);
    }).catch(error => {
      console.error('Failed to fetch locations:', error.message);
    });
  }

  return (
    <div className='container'>
      <h2>Book a Cab</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label className='label'>Source:</label>
          <input className='input' type="text" value={source} onChange={(e) => setSource(e.target.value)} required />
        </div>
        <div>
          <label className='label'>Destination:</label>
          <input className='input' type="text" value={destination} onChange={(e) => setDestination(e.target.value)} required />
        </div>
        <div>
          <label className='label'>Estimated Time:</label>
          <span>{estimatedTime} Minutes</span>
        </div>
        <div>
          <label className='label'>Email:</label>
          <input className='input' type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label className='label'>Date & Time:</label>
          <DatePicker selected={dateTime} onChange={(date) => setDateTime(date)} showTimeSelect dateFormat="yyyy-MM-dd HH:mm" required />
        </div>

        <div>
          <label className='label'>Select Cab:</label>
          <select value={selectedCab} onChange={(e) => setSelectedCab(e.target.value)} required>
            <option value="">Select cab</option>
            {cabList && cabList.map(cab => (
              <option key={cab.cab_id} value={cab.cab_id}>Cab {cab.cab_id} : (PPM : {cab.price_per_minute})</option>
            ))}
          </select>

          <label className='label'>Estimated Cost:</label>
          <span>Rs. {estimatedCost}</span>
        </div>
        <div>
          <button className='submit-btn' type="submit">Book Cab</button>
        </div>
      </form>
    </div>
  );
};




export default BookingForm;
