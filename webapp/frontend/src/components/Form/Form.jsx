import React, { useCallback, useEffect, useState } from 'react';
import './Form.css';
import { useTelegram } from '../../hooks/useTelegram';
import { useLocation } from 'react-router-dom';
import { strToBase64 } from '../../hooks/base64'

const Form = () => {
    const { tg } = useTelegram();
    const [Error, setError] = useState(false);

    cosnt [ login, setLogin ] = useState('');
    cosnt [ password, setPassword ] = useState('');
    cosnt [ key, setKey ] = useState('');

    const onSendData = useCallback(() => {
        const data = {
            login,
            password,
            key: strToBase64(key)
        };
        tg.sendData(JSON.stringify(data));
    }, [login, password, key]);
        
    tg.close();

    useEffect(() => {
        tg.onEvent('mainButtonClicked', onSendData);
        return () => {
            tg.offEvent('mainButtonClicked', onSendData);
        };
    }, [onSendData]);

    useEffect(() => {
        tg.MainButton.setParams({
            text: 'Отправить данные'
        });
    }, [tg.MainButton]);

    useEffect(() => {
        if (!login || !password || !key) {
            tg.MainButton.hide();
        } else {
            tg.MainButton.show();
        }
    }, [login, password, key]);

    const onChangeLogin = (e) => { setLogin(e.target.value); };
    const onChangePassword = (e) => { setPassword(e.target.value); };
    const onChangeKey = (e) => { setKey(e.target.value); };


    // Функция прокрутки страницы вниз
    const scrollToBottom = () => {
        window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
    };

    useEffect(() => {
        // Добавляем обработчики событий
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focus', scrollToBottom);
        });

        window.addEventListener('resize', scrollToBottom);

        // Убираем обработчики событий при размонтировании компонента
        return () => {
            inputs.forEach(input => {
                input.removeEventListener('focus', scrollToBottom);
            });
            window.removeEventListener('resize', scrollToBottom);
        };
    }, []);

    return (
        <div className="form">
            <h3>Введите ваши данные</h3>
            <input
                className="input"
                type="text"
                placeholder="Логин"
                value={login}
                onChange={onChangeLogin}
            />
            <input
                className="input"
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={onChangePassword}
            />
            <input
                className="input"
                type="password"
                placeholder="Ключ шифрования"
                value={key}
                onChange={onChangeKey}
            />
        </div>
    );
};

export default Form;