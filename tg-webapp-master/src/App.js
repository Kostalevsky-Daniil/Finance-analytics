import React, {useCallback, useEffect, useState} from 'react';
import './App.css';
import Button from "./Components/Button/Button";
const tg = window.Telegram.WebApp;
function App() {

    const onClose = () => {
        tg.close()
    }

    const onToggleButton = () =>{
        if (tg.MainButton.isVisible) {
            tg.MainButton.hide();
        }
        else {
            tg.MainButton.show();
        }
    }

    const handleClick = () => {
        // Ваше сообщение
        alert("Кнопка нажата");
    };



    // const onSendData = useCallback(() => {
    //     // Ваше сообщение
    //     const data = chatId;
    //     tg.sendData("handleSubmitActive-----");
    // }, [])

    // useEffect(() => {
    //     tg.onEvent('mainButtonCliked', onSendData)
    //     return () => {
    //         tg.offEvent('mainButtonCliked', onSendData)
    //     }
    // }, []);


    const [chatIdData, setChatIdData] = useState('');
    const handleChange = (e) => {
        setChatIdData(e.target.value);
    };

    const handleSendData = () => {
        const data = chatIdData + ';sub';
        // console.log(data);
        tg.sendData(data);
    };

    const handleSendDataCreate = () => {
        const data = chatIdData + ';create';
        // console.log(data);
        tg.sendData(data);
    };
    // const handleSubmit = (e) => {
    //     e.preventDefault();
    //     // Здесь можно выполнить отправку chatId на сервер или другие действия с ним
    //     console.log('Chat ID:', chatId);
    //     // Очистка поля после отправки, если необходимо
    //     setChatId('');
    // };

    return (
        <div className="App">
            <h3>Enter the data</h3>

            <input
                className={'input'}
                type="text"
                placeholder={'Chat ID'}
                value={chatIdData}
                onChange={handleChange}
            />
            <h3></h3>
            <input
                className={'input'}
                type="text"
                placeholder={'Price'}
                value={chatIdData}
                onChange={handleChange}
            />
            <h3></h3>
            <input
                className={'input'}
                type="text"
                placeholder={'Maximum users'}
                value={chatIdData}
                onChange={handleChange}
            />
            <h3></h3>
            <input
                className={'input'}
                type="text"
                placeholder={'Description'}
                value={chatIdData}
                onChange={handleChange}
            />
            <h3></h3>
            {/*<button onClick={onClose}>Закрыть эту хрень</button>*/}
            {/*<Button title={'Закрыть эту хрень'} disable={false} onClick={onClose}/>*/}
            {/*<Button title={'кнопка снизу'} disable={false} onClick={onToggleButton}/>*/}
            {/*<Button title={'вывод сообщения'} disable={false} onClick={handleClick}/>*/}
            {/*<Button title={'subscribe'} disable={false} onClick={handleSendData}/>*/}
            <Button title={'create community'} disable={false} onClick={handleSendDataCreate}/>
        </div>
    )
}

export default App;