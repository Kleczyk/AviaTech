
import React from "react";
import { IonContent, IonPage, IonButton } from '@ionic/react';
import { useHistory } from "react-router-dom";

import './Home.scss';

const Home: React.FC = () => {
  const history = useHistory();

  return (
    <IonPage>
      <IonContent fullscreen className="ion-padding">
        <div className="home">
          <img src="/assets/icons/plane.png" alt="kalus" className="logo"/>
          <div className="caption">
            <p className="title">Koalas' airlines</p>
            <p className="subtitle">Best airlines</p>
          </div>
          <IonButton
            size="large"
            onClick={() => {
              history.push("/ticket");
            }}
          >
            Buy a ticket
          </IonButton>
          <IonButton >Create FaceID</IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Home;
