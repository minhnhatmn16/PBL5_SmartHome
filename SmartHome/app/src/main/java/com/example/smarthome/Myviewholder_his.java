package com.example.smarthome;

import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class Myviewholder_his extends RecyclerView.ViewHolder {
    ImageView imageView;
    TextView nameView;
    TextView timeView;
    public Myviewholder_his(@NonNull View itemView) {
        super(itemView);
        imageView = itemView.findViewById(R.id.image_his);
        nameView = itemView.findViewById(R.id.name_his);
        timeView = itemView.findViewById(R.id.time_his);
    }
}
