package com.example.smarthome;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.AdapterView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.squareup.picasso.Picasso;

import java.text.SimpleDateFormat;
import java.util.List;

public class MyApdapter_his extends RecyclerView.Adapter<Myviewholder_his> {
    private OnItemClickListener listener;
    Context context;
    List<Item_his> items;

    public MyApdapter_his(Context context, List<Item_his> items) {
        this.context = context;
        this.items = items;
    }

    @NonNull
    @Override
    public Myviewholder_his onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new Myviewholder_his(LayoutInflater.from(context).inflate(R.layout.item_view_his,parent,false));
    }

    @Override
    public void onBindViewHolder(@NonNull Myviewholder_his holder, int position) {
        holder.nameView.setText(items.get(position).getName());
        holder.timeView.setText(items.get(position).getTime());

        Item_his currentItem = items.get(position);
        holder.itemView.setOnClickListener(v -> {
            if (listener != null) {
                listener.onItemClick(currentItem);
            }
        });
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    public interface OnItemClickListener{
        void onItemClick(Item_his item);
    }
    public void setListener(OnItemClickListener listener) {
        this.listener = listener;
    }
}
