package com.uom.pimote;

import android.content.Context;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.TableRow;

public class RegularButtonManager {
	
	TCPClient tcp;
	Context c;
	LinearLayout layout;
	
	public RegularButtonManager(Context c, TCPClient tcp, LinearLayout layout){
		this.c = c;
		this.tcp = tcp;
		this.layout = layout;
	}
	
	public void addButtons(final String[] setup) {
		if (Integer.parseInt(setup[0]) == 1) { // REGULAR BUTTON
			Button button = new Button(c);
			button.setText(setup[2]);
			button.setOnClickListener(new OnClickListener() {
				public void onClick(View v) {
					if (tcp != null)
						tcp.sendMessage(setup[1] + "," + " ");
				}
			});
			layout.addView(button);
		} else if (Integer.parseInt(setup[0]) == 2) { // BUTTON WITH TEXT
			LinearLayout textButtonLayout = new LinearLayout(c);
			LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
					LayoutParams.WRAP_CONTENT);
			textButtonLayout.setLayoutParams(params);
			final EditText addText = new EditText(c);
			addText.setHint(setup[2]);
			LayoutParams params2 = new TableRow.LayoutParams(0,
					LayoutParams.WRAP_CONTENT, 1f);
			addText.setLayoutParams(params2);
			Button button = new Button(c);
			button.setText("Send");
			button.setGravity(3);
			button.setOnClickListener(new OnClickListener() {
				public void onClick(View v) {
					if (tcp != null)
						tcp.sendMessage(setup[1] + ","
								+ addText.getText().toString());
					addText.setText("");
				}
			});
			textButtonLayout.addView(addText);
			textButtonLayout.addView(button);
			layout.addView(textButtonLayout);
		}
	}
}
