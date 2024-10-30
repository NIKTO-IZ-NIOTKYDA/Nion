import React, { useCallback, useEffect, useState } from 'react';
import './Form.css';
import {useTelegram} from "../../hooks/useTelegram";
import { TextAnimator } from '../TextAnimator/TextAnimator'
import { AddNetSchool } from '../../hooks/api'

const Form = () => {
    const {tg, chat, onClose} = useTelegram();

    const [ login, setLogin ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ key, setKey ] = useState('');

    const onSendData = useCallback(() => {
        AddNetSchool(chat.id, login, password, key)
        .then(data => console.log('Success:', data))
        .catch(err => console.error('Failed:', err));
        
        onClose();
    })

    useEffect(() => {
        tg.onEvent('mainButtonClicked', onSendData)
        return () => {
          tg.offEvent('mainButtonClicked', onSendData)
        }
      }, [onSendData])

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

    tg.ready();
    tg.expand();
    
    return (
        <div className="form">
            <h3 className="text-info"><TextAnimator text="введите ваши данные" /></h3>
            <input
                className="input"
                type="text"
                placeholder="Логин"
                value={login}
                onChange={onChangeLogin}
                maxLength="1024"
            />
            <input
                className="input"
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={onChangePassword}
                maxLength="1024"
            />
            <input
                className="input"
                type="password"
                placeholder="Ключ для шифрования данных"
                value={key}
                onChange={onChangeKey}
                maxLength="1024"
            />
        </div>
    );
};

export default Form;