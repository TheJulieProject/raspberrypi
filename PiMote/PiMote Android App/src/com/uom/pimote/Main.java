package com.uom.pimote;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Main extends Activity implements OnClickListener {

	EditText ipField, portField;
	Button connect;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.landing_page);

		try {
			Bundle b = getIntent().getExtras();
			String problem = b.getString("pr");
			if(!problem.equals(""))
				Toast.makeText(this, problem, Toast.LENGTH_LONG).show();
		} catch (Exception e) {
		}

		ipField = (EditText) findViewById(R.id.ipAddress);
		portField = (EditText) findViewById(R.id.portNo);
        ipField.setText("192.168.0.9");
        portField.setText("8090");
		connect = (Button) findViewById(R.id.connectBtn);
		connect.setOnClickListener(this);
	}

	@Override
	public void onClick(View v) {
		try {
			String ip = ipField.getText().toString();
			String portNo = portField.getText().toString();
			if(ip == null || portNo == null) throw new Exception();
			int port = Integer.parseInt(portField.getText().toString());
			Intent i = new Intent(this, Communicator.class);
			Bundle b = new Bundle();
			b.putString("ip", ip);
			b.putInt("port", port);
			i.putExtras(b);
			startActivity(i);
			finish();
		} catch (Exception e) {
			Toast.makeText(this, "Please input a valid IP and Port Number",
					Toast.LENGTH_LONG).show();
		}
	}

}
