package com.uom.pimote;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.LinearLayout;

public class Communicator extends Activity {

	TCPClient tcp;

	String ip;
	int port;
	LinearLayout layout;

	private static final int NORMAL_CONTROL = 0;
	private static final int JOYSTICK_CONTROL = 1;

	AsyncTask<String, String, TCPClient> task;

	RegularButtonManager regular = null;
	ControllerManager cm = null;

	boolean setup = false;
	private static int controlType = -1;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		try {
			Bundle b = getIntent().getExtras();
			port = b.getInt("port");
			ip = b.getString("ip");
		} catch (Exception e) {
			endActivity("Bad Arguments");
		}
		layout = (LinearLayout) findViewById(R.id.mainlayout);
		task = new connectTask().execute("");
	}

	public class connectTask extends AsyncTask<String, String, TCPClient> {

		@Override
		protected TCPClient doInBackground(String... message) {

			// we create a TCPClient object and
			tcp = new TCPClient(new TCPClient.OnMessageReceived() {
				@Override
				// here the messageReceived method is implemented
				public void messageReceived(String message) {
					// this method calls the onProgressUpdate
					publishProgress(message);
				}

				public void failActivity(String msg) {
					endActivity(msg);
				}
			}, ip, port);
			tcp.run();

			return null;
		}

		@Override
		protected void onProgressUpdate(String... values) {
			super.onProgressUpdate(values);
			final String[] info = values[0].split(",");
			// Log.d("pi", info[0] + ", " + info[1]);

			if (!setup) {
				Log.e("TCPClient", "Setting up");
				controlType = Integer.parseInt(info[0]);
				if (controlType == JOYSTICK_CONTROL)
					cm = new ControllerManager(Communicator.this, tcp,
							Integer.parseInt(info[1]));
				else
					regular = new RegularButtonManager(Communicator.this, tcp,
							layout);
				setup = true;
			} else {
				if (controlType == NORMAL_CONTROL) {
					regular.addButtons(info);
				}

			}
		}
	}

	protected void onPause() {
		super.onPause();
		finish();
	}

	@Override
	protected void onStop() {
		super.onStop();
		Log.d("pi", "Ending");
		tcp.stopClient();
		task.cancel(true);
	}

	public void endActivity(String msg) {
		Intent i = new Intent(this, Main.class);
		Bundle b = new Bundle();
		b.putString("pr", msg);
		i.putExtras(b);
		startActivity(i);
		finish();
	}

	@Override
	public void onBackPressed() {
		endActivity("");
	}
}
