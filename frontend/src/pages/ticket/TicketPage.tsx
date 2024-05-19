
import React, { useState } from "react";
import { IonContent, IonPage, IonButton, IonHeader, IonToolbar, IonTitle, IonItem, IonSelect, IonSelectOption, IonText, IonDatetime } from '@ionic/react';
import { useHistory } from "react-router-dom";
import { formatISO } from 'date-fns';

import './TicketPage.scss';

const TicketPage: React.FC = () => {
  const history = useHistory();
  const airPorts = ["Rzeszów", "Wąchock", "Kraków", "Warszawa"];
  const [startAirport, setStartAirport] = useState();
  const [destinyAirport, setDestinyAirport] = useState();
  const [ticketDate, setTicketDate] = useState(formatISO(Date.now()));

  const isWeekday = (dateString: string) => {
    const date = new Date(dateString);
    const utcDay = date.getUTCDay();
    return utcDay !== 0 && utcDay !== 6;
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Choose route</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <div className="select-wrap">
          <IonItem>
            <IonSelect
              placeholder="Select a start airport"
              onIonChange={e => setStartAirport(e.detail.value)}
            >
              <div slot="label">
                From <IonText color="danger">*</IonText>
              </div>
              {airPorts.filter(item => item != destinyAirport)
                .map(item => (
                  <IonSelectOption value={item}>{item}</IonSelectOption>
                )
              )}
            </IonSelect>
          </IonItem>
          <IonItem>
            <IonSelect
              placeholder="Select a destiny airport"
              onIonChange={e => setDestinyAirport(e.detail.value)}
            >
              <div slot="label">
                To <IonText color="danger">*</IonText>
              </div>
              {airPorts.filter(item => item != startAirport)
                .map(item => (
                  <IonSelectOption value={item}>{item}</IonSelectOption>
                )
              )}
            </IonSelect>
          </IonItem>
          <IonDatetime
            value={ticketDate}
            isDateEnabled={isWeekday}
            showDefaultButtons={true}
          >
          </IonDatetime>
          <IonButton
            size="large"
            onClick={() => {
              history.push("/faceid");
            }}
          >
            Select & Pay
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default TicketPage;
