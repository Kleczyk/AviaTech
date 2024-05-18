import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton } from '@ionic/react';

import './Home.scss';

const Home: React.FC = () => {
  return (
    <IonPage>
      <IonContent fullscreen className="ion-padding">
        <div className="home">
          <img src="/assets/icons/koalus.jpg" alt="kalus" className="logo"/>
          <div className="caption">
            <p className="title">Best airlines</p>
            <p className="subtitle">Best koalas</p>
          </div>
          <IonButton
            size="large"
            onClick={() => {}}
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
