package com.uom.pimote;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.TableRow;
import android.widget.ToggleButton;
import android.widget.TextView;

public class RegularButtonManager {

    TCPClient tcp;
    Context c;
    LinearLayout layout;

    public RegularButtonManager(Context c, TCPClient tcp, LinearLayout layout) {
        this.c = c;
        this.tcp = tcp;
        this.layout = layout;
        ((Communicator) c).setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
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
        } else if (Integer.parseInt(setup[0]) == 3) {
            LinearLayout textButtonLayout = new LinearLayout(c);
            LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
                    LayoutParams.WRAP_CONTENT);
            textButtonLayout.setLayoutParams(params);
            TextView text = new TextView(c);
            text.setText(setup[2]);
            LayoutParams params2 = new TableRow.LayoutParams(0,
                    LayoutParams.WRAP_CONTENT, 1f);
            text.setLayoutParams(params2);
            ToggleButton button = new ToggleButton(c);
            boolean checked = Integer.parseInt(setup[3]) == 1;
            button.setChecked(checked);
            button.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View view) {
                    int tf = ((ToggleButton) view).isChecked() ? 1 : 0;
                    tcp.sendMessage(setup[1] + "," + tf);
                }
            });
            textButtonLayout.addView(text);
            textButtonLayout.addView(button);
            layout.addView(textButtonLayout);
        }
    }
}
