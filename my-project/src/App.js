import medi from './Logo.png';
import './App.css';


function App() {
  return (
    <div>
      <div className="navbar bg-gradient-to-r from-error to-warning text-primary-content">
        <a className="btn btn-ghost text-xl">Documentation</a>
      </div>
      <div className="hero bg-base-200 min-h-screen">
        <div className="hero-content flex-col lg:flex-row-reverse">
          <img
            src={medi}
            className="max-w-sm rounded-lg shadow-2xl" />
          <div>
            <br className=""></br>
            <h1 className="text-5xl font-bold text-error">Emergency Dispatch Detection</h1>
            <br className="py-9"></br>
            <h1 className="text-2xl text-base-400 font-bold">Meet Your Lifesaving Chatbot!</h1>
            <br className="py-3"></br>
            <p >
              Introducing our <b>cutting-edge chatbot</b>, designed with a powerful Retrieval-Augmented Generation (RAG) layer. This isn't just any chatbot – it's your <u>personal crisis responder</u>, ready to jump into action at a moment's notice.
            </p>
            <p>
              Need someone to talk to? Our chatbot <b>connects</b> you with the right people for support. Facing an emergency? It assesses the urgency and calls <b>911</b> for you! Plus, it guides you through essential steps to ensure you handle any situation like a pro.
            </p>
            <p>
              With our chatbot, you're <b>never alone.</b> Feel the confidence of knowing help is just a message away. Get ready to experience the future of crisis management!
            </p>

            <br className="py-5"></br>
            {/* Open the modal using document.getElementById('ID').showModal() method */}
            <button className="btn btn-primary" onClick={() => document.getElementById('my_modal_5').showModal()}>Chat With Us!</button>
            <dialog id="my_modal_5" className="modal modal-bottom sm:modal-middle">
              <div className="modal-box">
                <h3 className="font-bold text-lg">Please Record your problem</h3>
                <p className="py-4">Click Submit for our model to diagnose your problem, an alert will show up if we have called 911 on you're behalf</p>
                <div className="modal-action">
                  <article class="clip">
                    <audio controls></audio>
                  </article>

                  <form method="dialog">
                    <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg">Submit</button>
                  </form>
                </div>
              </div>
            </dialog>

          </div>
        </div>
      </div>
    </div>

  );
}



export default App;
