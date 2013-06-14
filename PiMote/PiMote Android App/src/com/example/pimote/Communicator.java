package com.example.pimote;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.LinearLayout;

import com.uom.pimote.R;

public class Communicator extends Activity {

	TCPClient tcp;

	String ip;
	int port;
	LinearLayout layout;

	AsyncTask<String, String, TCPClient> task;

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
			Log.d("pi", info[0] + ", " + info[1]);
			Button button = new Button(Communicator.this);
			button.setText(info[1]);
			//button.setOnClickListener(new OnClickListener() {
				//public void onClick(View v) {
					//if (tcp != null)
						//tcp.sendMessage(info[0]);
				//}
			//});
			button.setOnTouchListener(new RepeatListener(100, 100, new OnClickListener() {
				  @Override
				  public void onClick(View view) {
				    // the code to execute repeatedly
					  if(tcp!=null)
						  tcp.sendMessage(info[0]);
				  }
				}));

			layout.addView(button);

			// output.append("\nPi: "+values[0]);
		}
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
	public void onBackPressed(){
		endActivity("");
	}
}
